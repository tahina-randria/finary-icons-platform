"""
In-memory task store for generation tracking
Simple implementation without Redis/Celery for MVP
"""

from typing import Dict, Optional
from datetime import datetime
from app.models.generation import GenerationStatus, GenerationStatusEnum
from threading import Lock

class TaskStore:
    """Thread-safe in-memory task storage"""

    def __init__(self):
        self._tasks: Dict[str, dict] = {}
        self._lock = Lock()

    def create_task(self, task_id: str, source_type: str, source_data: dict) -> None:
        """Create a new task"""
        with self._lock:
            self._tasks[task_id] = {
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
        with self._lock:
            if task_id not in self._tasks:
                raise ValueError(f"Task {task_id} not found")

            task = self._tasks[task_id]

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

    def get_task(self, task_id: str) -> Optional[dict]:
        """Get task by ID"""
        with self._lock:
            return self._tasks.get(task_id)

    def task_exists(self, task_id: str) -> bool:
        """Check if task exists"""
        with self._lock:
            return task_id in self._tasks


# Global instance
task_store = TaskStore()
