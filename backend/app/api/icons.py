"""
Icon management endpoints
"""

from fastapi import APIRouter, HTTPException, Query, Path, status
from fastapi.responses import FileResponse
from typing import Optional, List
from app.models.icon import Icon, IconResponse, IconList, IconCategory
from app.core.logging import logger

router = APIRouter()


@router.get(
    "/icons",
    response_model=IconList,
    status_code=status.HTTP_200_OK,
    summary="List icons",
    description="Get paginated list of icons with optional filters"
)
async def list_icons(
    search: Optional[str] = Query(None, description="Search term for icon name or tags"),
    category: Optional[IconCategory] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
) -> IconList:
    """
    List icons with optional search and filtering

    - **search**: Search in icon names and tags
    - **category**: Filter by specific category
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page (max 100)
    """
    try:
        # TODO: Implement database query
        # For now, return empty list
        logger.info(f"Listing icons: search={search}, category={category}, page={page}")

        return IconList(
            icons=[],
            total=0,
            page=page,
            page_size=page_size,
            success=True
        )

    except Exception as e:
        logger.error(f"Error listing icons: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list icons: {str(e)}"
        )


@router.get(
    "/icons/{icon_id}",
    response_model=IconResponse,
    status_code=status.HTTP_200_OK,
    summary="Get icon",
    description="Get detailed information about a specific icon"
)
async def get_icon(
    icon_id: str = Path(..., description="Icon ID")
) -> IconResponse:
    """
    Get detailed information about a specific icon

    - **icon_id**: Unique icon identifier
    """
    try:
        # TODO: Implement database query
        logger.info(f"Getting icon: {icon_id}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Icon not found: {icon_id}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting icon {icon_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get icon: {str(e)}"
        )


@router.get(
    "/icons/{icon_id}/download",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    summary="Download icon",
    description="Download icon image in specified size"
)
async def download_icon(
    icon_id: str = Path(..., description="Icon ID"),
    size: str = Query("original", description="Image size: original, 2k, 1k")
) -> FileResponse:
    """
    Download icon image

    - **icon_id**: Unique icon identifier
    - **size**: Image size variant (original, 2k, 1k)
    """
    try:
        # TODO: Implement download from Supabase storage
        logger.info(f"Downloading icon: {icon_id}, size={size}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Icon not found: {icon_id}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading icon {icon_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download icon: {str(e)}"
        )
