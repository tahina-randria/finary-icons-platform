"""
Health check endpoint
"""

from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    environment: str
    version: str
    timestamp: datetime


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"],
    summary="Health check",
    description="Check if the API is running and responsive"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    Returns basic service information
    """
    return HealthResponse(
        status="healthy",
        environment=settings.ENVIRONMENT,
        version=settings.VERSION,
        timestamp=datetime.utcnow()
    )
