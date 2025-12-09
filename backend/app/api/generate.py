"""
Icon generation endpoints
"""

from fastapi import APIRouter, HTTPException, Path, status, BackgroundTasks
from app.models.generation import (
    GenerateConceptRequest,
    GenerateYouTubeRequest,
    GenerateResponse,
    GenerationStatus,
    GenerationStatusEnum
)
from app.core.logging import logger
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

        # TODO: Add background task for YouTube processing
        # background_tasks.add_task(process_youtube_generation, task_id, request)

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
        # TODO: Query task status from database/cache
        logger.info(f"Checking status for task: {task_id}")

        # Return mock status for now
        return GenerationStatus(
            task_id=task_id,
            status=GenerationStatusEnum.PENDING,
            progress=0,
            message="Task is in queue",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    except Exception as e:
        logger.error(f"Error getting task status {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task status: {str(e)}"
        )
