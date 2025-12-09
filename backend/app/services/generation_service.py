"""
AI Image Generation Service using Gemini 3 Pro Image (Nano Banana Pro)
"""

import google.generativeai as genai
from app.core.config import settings
from app.core.logging import logger
from typing import Optional, Dict, Any
import base64
from io import BytesIO


class GenerationService:
    """Service for generating icons using AI"""

    def __init__(self):
        """Initialize Gemini API"""
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            logger.info("Gemini API configured")
        else:
            logger.warning("Gemini API key not configured")

    def _build_prompt(
        self,
        concept: str,
        style: str = "finary-glass-3d",
        category: Optional[str] = None
    ) -> str:
        """
        Build detailed prompt for icon generation
        NO GROUND REFLECTION as specified
        """
        base_prompt = f"""Create a high-quality 3D icon representing: {concept}

Style requirements:
- Finary aesthetic: Glass morphism with depth and dimension
- Modern, minimalist, professional design
- Smooth gradients and subtle lighting
- Clean edges with slight rounded corners
- Floating in space with soft ambient lighting
- NO GROUND REFLECTION
- NO SHADOWS ON GROUND
- Transparent or solid color background only

Visual characteristics:
- Central composition, well-balanced
- Appropriate color scheme for {category if category else 'the concept'}
- Depth through layering and subtle 3D effects
- Professional icon suitable for financial/business context
- High detail and polish
- PNG format with transparency

The icon should be instantly recognizable and work well at various sizes."""

        return base_prompt

    def _build_animation_prompt(
        self,
        concept: str,
        style: str = "finary-glass-3d"
    ) -> str:
        """Build prompt for video animation"""
        return f"""Animation prompt for motion design:

Icon: {concept} (Finary glass 3D style)

Animation sequence (3-5 seconds):
1. Entry (0-1s): Gentle float in from above with subtle rotation
2. Idle (1-3s): Soft floating motion with slight scale breathing (0.98-1.02)
3. Highlight (3-4s): Gentle glow pulse and rotate 15 degrees
4. Exit (4-5s): Fade out with slight upward float

Effects:
- Smooth easing (ease-in-out)
- Subtle glass reflection animations
- Soft glow on interaction/highlight
- Maintain depth and 3D feeling throughout
- No ground shadows or reflections

Style: Professional, elegant, understated"""

    async def generate_icon(
        self,
        concept: str,
        style: str = "finary-glass-3d",
        category: Optional[str] = None,
        size: str = "2048x2048"
    ) -> Dict[str, Any]:
        """
        Generate icon using Gemini 3 Pro Image

        Returns:
            Dict with image_data (base64), prompt, and animation_prompt
        """
        try:
            prompt = self._build_prompt(concept, style, category)
            animation_prompt = self._build_animation_prompt(concept, style)

            logger.info(f"Generating icon for concept: {concept}")

            # Parse size
            width, height = map(int, size.split("x"))

            # Generate image using Gemini
            # Note: Using imagen-3.0-generate-001 (Nano Banana Pro)
            model = genai.GenerativeModel("imagen-3.0-generate-001")

            response = model.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="1:1",
                safety_filter_level="block_only_high",
                person_generation="allow_adult"
            )

            if not response.images:
                raise Exception("No images generated")

            # Get first image
            image = response.images[0]

            # Convert to base64
            image_bytes = image._pil_image.tobytes() if hasattr(image, '_pil_image') else image.data
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            logger.info(f"Successfully generated icon for: {concept}")

            return {
                "image_data": image_base64,
                "prompt": prompt,
                "animation_prompt": animation_prompt,
                "concept": concept,
                "style": style,
                "size": size
            }

        except Exception as e:
            logger.error(f"Failed to generate icon for {concept}: {str(e)}")
            raise

    async def generate_icon_batch(
        self,
        concepts: list[str],
        style: str = "finary-glass-3d",
        category: Optional[str] = None
    ) -> list[Dict[str, Any]]:
        """Generate multiple icons in batch"""
        results = []

        for concept in concepts:
            try:
                result = await self.generate_icon(concept, style, category)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to generate icon for {concept}: {str(e)}")
                results.append({
                    "concept": concept,
                    "error": str(e)
                })

        return results


# Singleton instance
generation_service = GenerationService()
