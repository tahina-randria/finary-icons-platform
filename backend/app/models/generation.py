"""
Generation request and response models
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class GenerationStatusEnum(str, Enum):
    """Status of icon generation task"""
    PENDING = "pending"
    PROCESSING = "processing"
    EXTRACTING_CONCEPTS = "extracting_concepts"
    GENERATING_IMAGES = "generating_images"
    REMOVING_BACKGROUNDS = "removing_backgrounds"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"


class ConceptPriority(str, Enum):
    """Priority level for extracted concepts"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ConceptExtraction(BaseModel):
    """Extracted concept from YouTube transcript"""
    name: str = Field(..., description="Concept name")
    category: str = Field(..., description="Concept category")
    priority: ConceptPriority = Field(..., description="Importance priority")
    visual_description: str = Field(..., description="Visual description for generation")
    context: Optional[str] = Field(None, description="Context from transcript")


class GenerateConceptRequest(BaseModel):
    """Request to generate icon from single concept"""
    concept: str = Field(..., description="Concept to generate icon for")
    category: Optional[str] = Field(None, description="Optional category override")
    style: str = Field(default="finary-glass-3d", description="Visual style")
    size: str = Field(default="2048x2048", description="Image size")
    include_animation_prompt: bool = Field(default=True, description="Generate video animation prompt")

    class Config:
        json_schema_extra = {
            "example": {
                "concept": "Bitcoin investment",
                "category": "finance_investissement",
                "style": "finary-glass-3d",
                "size": "2048x2048"
            }
        }


class GenerateYouTubeRequest(BaseModel):
    """Request to generate icons from YouTube video"""
    youtube_url: HttpUrl = Field(..., description="YouTube video URL")
    max_concepts: int = Field(default=30, description="Maximum concepts to extract")
    min_priority: ConceptPriority = Field(default=ConceptPriority.MEDIUM, description="Minimum priority level")
    style: str = Field(default="finary-glass-3d", description="Visual style")
    auto_generate: bool = Field(default=True, description="Auto-generate icons after extraction")

    class Config:
        json_schema_extra = {
            "example": {
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "max_concepts": 30,
                "min_priority": "medium",
                "auto_generate": True
            }
        }


class GenerationStatus(BaseModel):
    """Status of generation task"""
    task_id: str = Field(..., description="Unique task identifier")
    status: GenerationStatusEnum = Field(..., description="Current status")
    progress: int = Field(default=0, description="Progress percentage 0-100")
    message: Optional[str] = Field(None, description="Status message")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error: Optional[str] = Field(None, description="Error message if failed")

    # Results
    extracted_concepts: Optional[List[ConceptExtraction]] = None
    generated_icons: Optional[List[str]] = Field(None, description="List of generated icon IDs")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class GenerateResponse(BaseModel):
    """Response for generation request"""
    task_id: str = Field(..., description="Task ID for status tracking")
    status: GenerationStatusEnum = Field(..., description="Initial status")
    message: str = Field(..., description="Response message")
    estimated_time_seconds: Optional[int] = Field(None, description="Estimated completion time")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "gen_abc123xyz",
                "status": "pending",
                "message": "Generation task created successfully",
                "estimated_time_seconds": 120
            }
        }
