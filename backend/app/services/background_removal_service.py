"""
Background Removal Service using BRIA RMBG 2.0
Best background removal model 2025 with 8-bit alpha matting
"""

import replicate
from app.core.config import settings
from app.core.logging import logger
from typing import Optional
import base64
from io import BytesIO
from PIL import Image
import httpx


class BackgroundRemovalService:
    """Service for removing backgrounds using BRIA RMBG 2.0"""

    def __init__(self):
        """Initialize Replicate API"""
        if settings.REPLICATE_API_TOKEN:
            self.client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)
            logger.info("Replicate API configured for BRIA RMBG 2.0")
        else:
            self.client = None
            logger.warning("Replicate API token not configured")

    async def remove_background(
        self,
        image_data: bytes,
        output_format: str = "png"
    ) -> bytes:
        """
        Remove background using BRIA RMBG 2.0

        Args:
            image_data: Input image bytes
            output_format: Output format (png recommended for transparency)

        Returns:
            Image bytes with removed background
        """
        if not self.client:
            raise Exception("Replicate client not initialized")

        try:
            logger.info("Removing background with BRIA RMBG 2.0")

            # Convert bytes to base64 data URI
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            data_uri = f"data:image/png;base64,{image_b64}"

            # Run BRIA RMBG 2.0 model
            # This model provides 8-bit alpha matting (256 transparency levels)
            # +5-8 IoU points better than competitors
            # 50% fewer halo artifacts
            output = self.client.run(
                "briaai/RMBG-2.0:59626141ca33e4fb7cf0fbba36a2629d29aa4a728e7268abf314e0d8e16e7c9e",
                input={
                    "image": data_uri,
                    "output_format": output_format
                }
            )

            # Output is a URL to the processed image
            if isinstance(output, str):
                # Download the result
                async with httpx.AsyncClient() as client:
                    response = await client.get(output)
                    response.raise_for_status()
                    result_data = response.content
            else:
                result_data = output

            logger.info("Background removed successfully")
            return result_data

        except Exception as e:
            logger.error(f"Failed to remove background: {str(e)}")
            raise

    async def remove_background_from_base64(
        self,
        image_base64: str,
        output_format: str = "png"
    ) -> str:
        """
        Remove background from base64 image

        Returns:
            Base64 encoded image with removed background
        """
        try:
            # Decode base64
            image_data = base64.b64decode(image_base64)

            # Remove background
            result_data = await self.remove_background(image_data, output_format)

            # Encode back to base64
            result_base64 = base64.b64encode(result_data).decode('utf-8')

            return result_base64

        except Exception as e:
            logger.error(f"Failed to process base64 image: {str(e)}")
            raise

    async def process_with_fallback(
        self,
        image_data: bytes
    ) -> bytes:
        """
        Remove background with fallback to simple methods if API fails
        """
        try:
            # Try BRIA RMBG 2.0 first
            return await self.remove_background(image_data)

        except Exception as e:
            logger.warning(f"BRIA RMBG 2.0 failed, using fallback: {str(e)}")

            # Fallback: Use rembg library
            try:
                from rembg import remove
                image = Image.open(BytesIO(image_data))
                output = remove(image)

                # Convert back to bytes
                output_bytes = BytesIO()
                output.save(output_bytes, format='PNG')
                return output_bytes.getvalue()

            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                # Return original image if all fails
                return image_data


# Singleton instance
background_removal_service = BackgroundRemovalService()
