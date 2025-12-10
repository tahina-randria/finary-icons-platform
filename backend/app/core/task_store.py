"""
Task store for generation tracking with Redis backend
Falls back to in-memory storage when Redis is unavailable
"""

import json
import logging
from typing import Dict, Optional
from datetime import datetime
from threading import Lock
from app.models.generation import GenerationStatus, GenerationStatusEnum
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Try to import Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("redis package not available, using in-memory storage")


class RedisTaskStore:
    """Redis-backed task storage with fallback to in-memory"""

    # Task TTL in seconds (24 hours)
    TASK_TTL = 24 * 60 * 60

    def __init__(self):
        self._redis_client = None
        self._use_redis = False
        self._memory_tasks: Dict[str, dict] = {}
        self._lock = Lock()

        # Try to connect to Redis if available
        if REDIS_AVAILABLE and settings.REDIS_URL:
            try:
                self._redis_client = redis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
                # Test connection
                self._redis_client.ping()
                self._use_redis = True
                logger.info("Connected to Redis for task storage")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}. Using in-memory storage.")
                self._redis_client = None
                self._use_redis = False
        else:
            logger.info("Redis not configured, using in-memory task storage")

    def _get_redis_key(self, task_id: str) -> str:
        """Generate Redis key for task"""
        return f"task:{task_id}"

    def _serialize_task(self, task: dict) -> dict:
        """Serialize task for storage (convert datetime to ISO strings)"""
        serialized = task.copy()

        # Convert datetime objects to ISO format strings
        if isinstance(serialized.get("created_at"), datetime):
            serialized["created_at"] = serialized["created_at"].isoformat()
        if isinstance(serialized.get("updated_at"), datetime):
            serialized["updated_at"] = serialized["updated_at"].isoformat()
        if isinstance(serialized.get("completed_at"), datetime):
            serialized["completed_at"] = serialized["completed_at"].isoformat()

        # Convert enum to string
        if isinstance(serialized.get("status"), GenerationStatusEnum):
            serialized["status"] = serialized["status"].value

        return serialized

    def _deserialize_task(self, task: dict) -> dict:
        """Deserialize task from storage (convert ISO strings to datetime)"""
        deserialized = task.copy()

        # Convert ISO format strings back to datetime objects
        if isinstance(deserialized.get("created_at"), str):
            deserialized["created_at"] = datetime.fromisoformat(deserialized["created_at"])
        if isinstance(deserialized.get("updated_at"), str):
            deserialized["updated_at"] = datetime.fromisoformat(deserialized["updated_at"])
        if deserialized.get("completed_at") and isinstance(deserialized["completed_at"], str):
            deserialized["completed_at"] = datetime.fromisoformat(deserialized["completed_at"])

        # Convert string to enum
        if isinstance(deserialized.get("status"), str):
            deserialized["status"] = GenerationStatusEnum(deserialized["status"])

        return deserialized

    def create_task(self, task_id: str, source_type: str, source_data: dict) -> None:
        """Create a new task"""
        task = {
            "task_id": task_id,
            "status": GenerationStatusEnum.PENDING,
            "progress": 0,
            "message": "Task created",
            "source_type": source_type,
            "source_data": source_data,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "transcript": None,
            "transcript_text": None,
            "extracted_concepts": None,
            "generated_icons": None,
            "error": None
        }

        if self._use_redis:
            try:
                key = self._get_redis_key(task_id)
                serialized = self._serialize_task(task)
                self._redis_client.setex(
                    key,
                    self.TASK_TTL,
                    json.dumps(serialized)
                )
                logger.debug(f"Created task {task_id} in Redis")
                return
            except Exception as e:
                logger.error(f"Redis error creating task {task_id}: {e}. Falling back to memory.")
                # Fall back to in-memory storage
                self._use_redis = False

        # In-memory storage (fallback or default)
        with self._lock:
            self._memory_tasks[task_id] = task
            logger.debug(f"Created task {task_id} in memory")

    def update_task(
        self,
        task_id: str,
        status: Optional[GenerationStatusEnum] = None,
        progress: Optional[int] = None,
        message: Optional[str] = None,
        transcript: Optional[list] = None,
        extracted_concepts: Optional[list] = None,
        generated_icons: Optional[list] = None,
        error: Optional[str] = None
    ) -> None:
        """Update task fields"""
        if self._use_redis:
            try:
                key = self._get_redis_key(task_id)
                task_json = self._redis_client.get(key)

                if not task_json:
                    raise ValueError(f"Task {task_id} not found")

                task = json.loads(task_json)
                task = self._deserialize_task(task)

                # Update fields
                if status is not None:
                    task["status"] = status
                if progress is not None:
                    task["progress"] = progress
                if message is not None:
                    task["message"] = message
                if transcript is not None:
                    task["transcript"] = transcript
                if extracted_concepts is not None:
                    task["extracted_concepts"] = extracted_concepts
                if generated_icons is not None:
                    task["generated_icons"] = generated_icons
                if error is not None:
                    task["error"] = error
                    task["status"] = GenerationStatusEnum.FAILED

                task["updated_at"] = datetime.utcnow()

                if status == GenerationStatusEnum.COMPLETED:
                    task["completed_at"] = datetime.utcnow()

                # Save back to Redis
                serialized = self._serialize_task(task)
                self._redis_client.setex(
                    key,
                    self.TASK_TTL,
                    json.dumps(serialized)
                )
                logger.debug(f"Updated task {task_id} in Redis")
                return
            except ValueError:
                # Task not found - re-raise
                raise
            except Exception as e:
                logger.error(f"Redis error updating task {task_id}: {e}. Falling back to memory.")
                self._use_redis = False

        # In-memory storage (fallback or default)
        with self._lock:
            if task_id not in self._memory_tasks:
                raise ValueError(f"Task {task_id} not found")

            task = self._memory_tasks[task_id]

            if status is not None:
                task["status"] = status
            if progress is not None:
                task["progress"] = progress
            if message is not None:
                task["message"] = message
            if transcript is not None:
                task["transcript"] = transcript
            if extracted_concepts is not None:
                task["extracted_concepts"] = extracted_concepts
            if generated_icons is not None:
                task["generated_icons"] = generated_icons
            if error is not None:
                task["error"] = error
                task["status"] = GenerationStatusEnum.FAILED

            task["updated_at"] = datetime.utcnow()

            if status == GenerationStatusEnum.COMPLETED:
                task["completed_at"] = datetime.utcnow()

            logger.debug(f"Updated task {task_id} in memory")

    def get_task(self, task_id: str) -> Optional[dict]:
        """Get task by ID"""
        if self._use_redis:
            try:
                key = self._get_redis_key(task_id)
                task_json = self._redis_client.get(key)

                if task_json:
                    task = json.loads(task_json)
                    task = self._deserialize_task(task)
                    logger.debug(f"Retrieved task {task_id} from Redis")
                    return task
                return None
            except Exception as e:
                logger.error(f"Redis error getting task {task_id}: {e}. Falling back to memory.")
                self._use_redis = False

        # In-memory storage (fallback or default)
        with self._lock:
            task = self._memory_tasks.get(task_id)
            if task:
                logger.debug(f"Retrieved task {task_id} from memory")
            return task

    def task_exists(self, task_id: str) -> bool:
        """Check if task exists"""
        if self._use_redis:
            try:
                key = self._get_redis_key(task_id)
                exists = self._redis_client.exists(key) > 0
                logger.debug(f"Task {task_id} exists in Redis: {exists}")
                return exists
            except Exception as e:
                logger.error(f"Redis error checking task {task_id}: {e}. Falling back to memory.")
                self._use_redis = False

        # In-memory storage (fallback or default)
        with self._lock:
            exists = task_id in self._memory_tasks
            logger.debug(f"Task {task_id} exists in memory: {exists}")
            return exists


# Global instance
task_store = RedisTaskStore()
