"""Design Schemas"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class DesignCreate(BaseModel):
    """Schema for creating a new design"""
    prompt: str = Field(..., description="Natural language description")
    component_type: Optional[str] = Field(None, description="Type of component (wing, fuselage, etc.)")
    name: Optional[str] = Field(None, description="Design name")
    is_public: bool = Field(True, description="Make design public")
    allow_learning: bool = Field(True, description="Allow AI to learn from this design")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Manual parameters (optional)")


class DesignUpdate(BaseModel):
    """Schema for updating a design"""
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    allow_learning: Optional[bool] = None


class ParameterSchema(BaseModel):
    """Schema for design parameters"""
    name: str
    display_name: Optional[str] = None
    parameter_type: str
    value: Optional[float] = None
    value_string: Optional[str] = None
    unit: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    description: Optional[str] = None


class ValidationResult(BaseModel):
    """Schema for validation results"""
    valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    analysis: Dict[str, Any] = {}


class DesignResponse(BaseModel):
    """Schema for design response"""
    id: int
    owner_id: int
    name: str
    description: Optional[str] = None
    component_type: str
    prompt: Optional[str] = None
    is_public: bool
    allow_learning: bool
    parameters: Optional[Dict[str, Any]] = None
    cad_file_path: Optional[str] = None
    cad_format: Optional[str] = None
    thumbnail_path: Optional[str] = None
    file_size_mb: float
    is_validated: bool
    validation_results: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    version: int
    downloads: int
    likes: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExportRequest(BaseModel):
    """Schema for export request"""
    format: str = Field(..., description="Export format (step, iges, stl, obj)")
    include_assembly: bool = Field(False, description="Include full assembly")


class ExportResponse(BaseModel):
    """Schema for export response"""
    success: bool
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    file_size_mb: Optional[float] = None
    format: str
    error: Optional[str] = None
