"""
YouTube generation background worker
Processes YouTube URL extraction and icon generation
"""

import asyncio
from app.core.logging import logger
from app.core.task_store import task_store
from app.models.generation import GenerationStatusEnum
from app.services.youtube_service import YouTubeService
from app.services.concept_extraction_service import ConceptExtractionService
from app.services.generation_service import GenerationService
from app.services.background_removal_service import BackgroundRemovalService
from app.services.supabase_service import SupabaseService


async def process_youtube_generation(
    task_id: str,
    youtube_url: str,
    max_concepts: int = 10,
    auto_generate: bool = True
):
    """
    Process YouTube video for concept extraction and icon generation

    Args:
        task_id: Unique task identifier
        youtube_url: YouTube video URL
        max_concepts: Maximum number of concepts to extract
        auto_generate: Whether to automatically generate icons
    """
    try:
        logger.info(f"[{task_id}] Starting YouTube processing for {youtube_url}")

        # Initialize services
        youtube_service = YouTubeService()
        concept_service = ConceptExtractionService()
        generation_service = GenerationService()
        bg_removal_service = BackgroundRemovalService()
        supabase_service = SupabaseService()

        # Step 1: Extract transcript (0-20%)
        task_store.update_task(
            task_id,
            status=GenerationStatusEnum.PROCESSING,
            progress=5,
            message="Extracting YouTube transcript..."
        )

        transcript = await youtube_service.get_transcript(youtube_url)
        if not transcript:
            raise Exception("Failed to extract transcript from YouTube video")

        logger.info(f"[{task_id}] Extracted {len(transcript)} transcript segments")

        # Convert transcript to format for frontend
        transcript_segments = [
            {"text": seg["text"], "start": seg["start"], "duration": seg["duration"]}
            for seg in transcript
        ]

        task_store.update_task(
            task_id,
            progress=20,
            message=f"Transcript extracted ({len(transcript)} segments)",
            transcript=transcript_segments
        )

        # Step 2: Extract concepts with GPT-4 (20-40%)
        task_store.update_task(
            task_id,
            status=GenerationStatusEnum.EXTRACTING_CONCEPTS,
            progress=25,
            message="Analyzing transcript with GPT-4..."
        )

        transcript_text = " ".join([seg["text"] for seg in transcript])
        concepts = await concept_service.extract_concepts(
            transcript_text,
            max_concepts=max_concepts
        )

        if not concepts:
            raise Exception("No concepts could be extracted from the transcript")

        logger.info(f"[{task_id}] Extracted {len(concepts)} concepts")

        # Convert concepts to frontend format
        concept_list = [
            {
                "name": c.name,
                "category": c.category,
                "priority": c.priority,
                "visual_description": c.visual_description,
                "context": c.context
            }
            for c in concepts
        ]

        task_store.update_task(
            task_id,
            progress=40,
            message=f"Extracted {len(concepts)} concepts",
            extracted_concepts=concept_list
        )

        if not auto_generate:
            task_store.update_task(
                task_id,
                status=GenerationStatusEnum.COMPLETED,
                progress=100,
                message=f"Concept extraction completed. {len(concepts)} concepts ready for generation."
            )
            return

        # Step 3: Generate icons for each concept (40-80%)
        task_store.update_task(
            task_id,
            status=GenerationStatusEnum.GENERATING_IMAGES,
            progress=45,
            message="Starting icon generation..."
        )

        generated_icon_ids = []
        generated_concepts = []  # Track successfully generated concepts
        total_concepts = len(concepts)

        for idx, concept in enumerate(concepts):
            try:
                # Update progress
                progress = 45 + int((idx / total_concepts) * 35)
                task_store.update_task(
                    task_id,
                    progress=progress,
                    message=f"Generating icon {idx + 1}/{total_concepts}: {concept.name}",
                    generated_icons=generated_icon_ids
                )

                # Generate image with Gemini
                logger.info(f"[{task_id}] Generating icon for: {concept.name}")
                image_data = await generation_service.generate_icon_from_concept(
                    concept=concept.name,
                    category=concept.category,
                    visual_description=concept.visual_description
                )

                if image_data:
                    # Mark this concept as successfully generated
                    generated_concepts.append(concept.name)
                    # Step 4: Remove background (per icon) - skip if Replicate not configured
                    processed_image = image_data
                    if bg_removal_service.client:
                        try:
                            logger.info(f"[{task_id}] Removing background for: {concept.name}")
                            processed_image = await bg_removal_service.remove_background(image_data)
                        except Exception as bg_error:
                            logger.warning(f"[{task_id}] Background removal failed for {concept.name}: {str(bg_error)}")
                            logger.info(f"[{task_id}] Using original image without background removal")
                    else:
                        logger.info(f"[{task_id}] Skipping background removal (Replicate not configured)")

                    # Step 5: Upload image to Supabase storage
                    logger.info(f"[{task_id}] Uploading image to storage: {concept.name}")
                    import time
                    import uuid
                    file_name = f"{concept.name.lower().replace(' ', '_')}_{int(time.time())}_{uuid.uuid4().hex[:8]}.png"

                    try:
                        image_url = await supabase_service.upload_image(
                            file_data=processed_image,
                            file_name=file_name
                        )

                        # Create icon record in database
                        logger.info(f"[{task_id}] Creating icon record: {concept.name}")
                        icon_result = await supabase_service.create_icon({
                            "name": concept.name,
                            "category": concept.category,
                            "prompt": concept.visual_description,
                            "image_url": image_url,
                            "tags": [concept.category, concept.priority]
                        })

                        icon_id = icon_result.get("id")
                        if icon_id:
                            generated_icon_ids.append(icon_id)
                            logger.info(f"[{task_id}] Icon created with ID: {icon_id}")

                    except Exception as upload_error:
                        logger.error(f"[{task_id}] Supabase upload/create failed for {concept.name}: {str(upload_error)}")
                        logger.info(f"[{task_id}] Skipping Supabase (not configured), continuing with next concept")

            except Exception as e:
                logger.error(f"[{task_id}] Error generating icon for {concept.name}: {str(e)}")
                # Continue with next concept
                continue

        # Step 6: Complete
        if not generated_concepts:
            raise Exception("Failed to generate any icons")

        # Success message depends on whether we have Supabase configured
        if generated_icon_ids:
            message = f"Successfully generated and stored {len(generated_icon_ids)} icons!"
        else:
            message = f"Successfully generated {len(generated_concepts)} icons! (Supabase not configured - icons not stored)"

        task_store.update_task(
            task_id,
            status=GenerationStatusEnum.COMPLETED,
            progress=100,
            message=message,
            generated_icons=generated_icon_ids
        )

        logger.info(f"[{task_id}] YouTube generation completed. Generated {len(generated_concepts)} icons ({len(generated_icon_ids)} stored).")

    except Exception as e:
        error_msg = f"YouTube generation failed: {str(e)}"
        logger.error(f"[{task_id}] {error_msg}")
        task_store.update_task(
            task_id,
            status=GenerationStatusEnum.FAILED,
            error=error_msg,
            message=error_msg
        )
