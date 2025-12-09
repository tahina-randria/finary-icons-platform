"""
Supabase database and storage service
"""

from supabase import create_client, Client
from app.core.config import settings
from app.core.logging import logger
from typing import Optional, List, Dict, Any
import base64
from io import BytesIO


class SupabaseService:
    """Service for interacting with Supabase"""

    def __init__(self):
        """Initialize Supabase client"""
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            logger.warning("Supabase credentials not configured")
            self.client: Optional[Client] = None
        else:
            self.client: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_KEY
            )
            logger.info("Supabase client initialized")

    # ===== Icons Table Operations =====

    async def create_icon(self, icon_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new icon record"""
        if not self.client:
            raise Exception("Supabase client not initialized")

        try:
            result = self.client.table("icons").insert(icon_data).execute()
            logger.info(f"Created icon: {result.data[0].get('id')}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Failed to create icon: {str(e)}")
            raise

    async def get_icon(self, icon_id: str) -> Optional[Dict[str, Any]]:
        """Get icon by ID"""
        if not self.client:
            raise Exception("Supabase client not initialized")

        try:
            result = self.client.table("icons").select("*").eq("id", icon_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Failed to get icon {icon_id}: {str(e)}")
            raise

    async def list_icons(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        offset: int = 0,
        limit: int = 20
    ) -> tuple[List[Dict[str, Any]], int]:
        """List icons with pagination and filters"""
        if not self.client:
            raise Exception("Supabase client not initialized")

        try:
            query = self.client.table("icons").select("*", count="exact")

            # Apply filters
            if search:
                query = query.or_(f"name.ilike.%{search}%,tags.cs.{{{search}}}")
            if category:
                query = query.eq("category", category)

            # Apply pagination
            query = query.range(offset, offset + limit - 1).order("created_at", desc=True)

            result = query.execute()
            total = result.count if result.count else 0

            return result.data, total

        except Exception as e:
            logger.error(f"Failed to list icons: {str(e)}")
            raise

    async def update_icon(self, icon_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update icon record"""
        if not self.client:
            raise Exception("Supabase client not initialized")

        try:
            result = self.client.table("icons").update(updates).eq("id", icon_id).execute()
            logger.info(f"Updated icon: {icon_id}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Failed to update icon {icon_id}: {str(e)}")
            raise

    async def increment_download_count(self, icon_id: str):
        """Increment download counter for icon"""
        if not self.client:
            return

        try:
            self.client.rpc("increment_download_count", {"icon_id": icon_id}).execute()
        except Exception as e:
            logger.error(f"Failed to increment download count: {str(e)}")

    # ===== Storage Operations =====

    async def upload_image(
        self,
        file_data: bytes,
        file_name: str,
        bucket: str = "icons",
        content_type: str = "image/png"
    ) -> str:
        """Upload image to Supabase storage"""
        if not self.client:
            raise Exception("Supabase client not initialized")

        try:
            result = self.client.storage.from_(bucket).upload(
                path=file_name,
                file=file_data,
                file_options={"content-type": content_type}
            )

            # Get public URL
            url = self.client.storage.from_(bucket).get_public_url(file_name)
            logger.info(f"Uploaded image: {file_name}")
            return url

        except Exception as e:
            logger.error(f"Failed to upload image {file_name}: {str(e)}")
            raise

    async def upload_image_from_base64(
        self,
        base64_data: str,
        file_name: str,
        bucket: str = "icons"
    ) -> str:
        """Upload image from base64 string"""
        try:
            # Decode base64
            image_data = base64.b64decode(base64_data)
            return await self.upload_image(image_data, file_name, bucket)
        except Exception as e:
            logger.error(f"Failed to upload from base64: {str(e)}")
            raise

    async def get_download_url(self, file_path: str, bucket: str = "icons", expires_in: int = 3600) -> str:
        """Get signed URL for file download"""
        if not self.client:
            raise Exception("Supabase client not initialized")

        try:
            result = self.client.storage.from_(bucket).create_signed_url(
                path=file_path,
                expires_in=expires_in
            )
            return result["signedURL"]
        except Exception as e:
            logger.error(f"Failed to get download URL: {str(e)}")
            raise

    # ===== Generation Tasks =====

    async def create_generation_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create generation task record"""
        if not self.client:
            raise Exception("Supabase client not initialized")

        try:
            result = self.client.table("generations").insert(task_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Failed to create generation task: {str(e)}")
            raise

    async def update_generation_task(self, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update generation task"""
        if not self.client:
            raise Exception("Supabase client not initialized")

        try:
            result = self.client.table("generations").update(updates).eq("task_id", task_id).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Failed to update generation task: {str(e)}")
            raise

    async def get_generation_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get generation task by ID"""
        if not self.client:
            raise Exception("Supabase client not initialized")

        try:
            result = self.client.table("generations").select("*").eq("task_id", task_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Failed to get generation task: {str(e)}")
            raise


# Singleton instance
supabase_service = SupabaseService()
