"""
Icon generation endpoints
"""

import asyncio
from fastapi import APIRouter, HTTPException, Path, status, BackgroundTasks
from app.models.generation import (
    GenerateConceptRequest,
    GenerateYouTubeRequest,
    GenerateResponse,
    GenerationStatus,
    GenerationStatusEnum
)
from app.core.logging import logger
from app.core.task_store import task_store
from app.workers.youtube_worker import process_youtube_generation
import uuid
from datetime import datetime

router = APIRouter()


@router.post(
    "/generate/concept",
    response_model=GenerateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate from concept",
    description="Generate icon from a single concept/text"
)
async def generate_from_concept(
    request: GenerateConceptRequest,
    background_tasks: BackgroundTasks
) -> GenerateResponse:
    """
    Generate icon from a text concept

    - **concept**: The concept to visualize (e.g., "Bitcoin investment")
    - **category**: Optional category override
    - **style**: Visual style (default: finary-glass-3d)
    - **size**: Image dimensions
    """
    try:
        # Generate unique task ID
        task_id = f"gen_{uuid.uuid4().hex[:12]}"

        logger.info(f"Creating generation task {task_id} for concept: {request.concept}")

        # Create task in store
        task_store.create_task(
            task_id=task_id,
            source_type="concept",
            source_data={"concept": request.concept}
        )

        # TODO: Add background task for actual generation
        # background_tasks.add_task(process_concept_generation, task_id, request)

        return GenerateResponse(
            task_id=task_id,
            status=GenerationStatusEnum.PENDING,
            message=f"Generation task created for concept: {request.concept}",
            estimated_time_seconds=60
        )

    except Exception as e:
        logger.error(f"Error creating generation task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create generation task: {str(e)}"
        )


@router.post(
    "/generate/youtube",
    response_model=GenerateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generate from YouTube",
    description="Extract concepts from YouTube video and generate icons"
)
async def generate_from_youtube(
    request: GenerateYouTubeRequest,
    background_tasks: BackgroundTasks
) -> GenerateResponse:
    """
    Generate icons from YouTube video transcript

    - **youtube_url**: YouTube video URL
    - **max_concepts**: Maximum number of concepts to extract
    - **min_priority**: Minimum priority level for concepts
    - **auto_generate**: Automatically generate icons after extraction
    """
    try:
        # Generate unique task ID
        task_id = f"gen_yt_{uuid.uuid4().hex[:12]}"

        logger.info(f"Creating YouTube generation task {task_id} for URL: {request.youtube_url}")

        # Create task in store
        task_store.create_task(
            task_id=task_id,
            source_type="youtube",
            source_data={
                "youtube_url": request.youtube_url,
                "max_concepts": request.max_concepts,
                "auto_generate": request.auto_generate
            }
        )

        # Launch background task
        background_tasks.add_task(
            process_youtube_generation,
            task_id=task_id,
            youtube_url=request.youtube_url,
            max_concepts=request.max_concepts,
            auto_generate=request.auto_generate
        )

        estimated_time = request.max_concepts * 3 if request.auto_generate else 30

        return GenerateResponse(
            task_id=task_id,
            status=GenerationStatusEnum.PENDING,
            message=f"YouTube processing task created. Will extract up to {request.max_concepts} concepts.",
            estimated_time_seconds=estimated_time
        )

    except Exception as e:
        logger.error(f"Error creating YouTube generation task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create YouTube generation task: {str(e)}"
        )


@router.get(
    "/generate/status/{task_id}",
    response_model=GenerationStatus,
    status_code=status.HTTP_200_OK,
    summary="Get generation status",
    description="Check status of a generation task"
)
async def get_generation_status(
    task_id: str = Path(..., description="Task ID")
) -> GenerationStatus:
    """
    Get the current status of a generation task

    - **task_id**: Task identifier returned from generation request
    """
    try:
        logger.info(f"Checking status for task: {task_id}")

        # Get task from store
        task_data = task_store.get_task(task_id)

        if not task_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )

        # Return task status
        return GenerationStatus(
            task_id=task_data["task_id"],
            status=task_data["status"],
            progress=task_data["progress"],
            message=task_data.get("message"),
            created_at=task_data["created_at"],
            updated_at=task_data["updated_at"],
            completed_at=task_data.get("completed_at"),
            error=task_data.get("error"),
            transcript=task_data.get("transcript"),
            extracted_concepts=task_data.get("extracted_concepts"),
            generated_icons=task_data.get("generated_icons")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task status {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task status: {str(e)}"
        )
