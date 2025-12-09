"""
Icon data models and schemas
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum


class IconCategory(str, Enum):
    """Icon categories based on concept extraction"""
    FINANCE_INVESTISSEMENT = "finance_investissement"
    IMMOBILIER = "immobilier"
    VEHICULES = "vehicules"
    METIERS = "metiers"
    OBJETS = "objets"
    LIEUX = "lieux"
    DEVISES = "devises"
    ACTIONS = "actions"
    ETATS = "etats"
    ORGANISMES = "organismes"
    NOURRITURE = "nourriture"
    SPORT = "sport"
    OTHER = "other"


class IconBase(BaseModel):
    """Base icon schema"""
    name: str = Field(..., description="Icon name/concept")
    category: IconCategory = Field(..., description="Icon category")
    prompt: str = Field(..., description="Generation prompt used")
    animation_prompt: Optional[str] = Field(None, description="Video animation prompt")
    tags: List[str] = Field(default_factory=list, description="Searchable tags")


class IconCreate(IconBase):
    """Schema for creating a new icon"""
    image_data: Optional[str] = Field(None, description="Base64 encoded image data")


class Icon(IconBase):
    """Full icon model with database fields"""
    id: str = Field(..., description="Unique icon ID")
    image_url: HttpUrl = Field(..., description="URL to icon image")
    thumbnail_url: Optional[HttpUrl] = Field(None, description="URL to thumbnail")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    download_count: int = Field(default=0, description="Number of downloads")

    class Config:
        from_attributes = True


class IconResponse(BaseModel):
    """API response for single icon"""
    icon: Icon
    success: bool = True
    message: Optional[str] = None


class IconList(BaseModel):
    """API response for icon list"""
    icons: List[Icon]
    total: int
    page: int
    page_size: int
    success: bool = True


class IconDownload(BaseModel):
    """Icon download request"""
    icon_id: str
    size: str = Field(default="original", description="Image size: original, 2k, 1k")

    class Config:
        json_schema_extra = {
            "example": {
                "icon_id": "abc123",
                "size": "2k"
            }
        }
