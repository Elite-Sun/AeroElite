"""Assembly Schemas"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ComponentPosition(BaseModel):
    """Schema for component position"""
    design_id: int
    component_name: str
    position_x: float = 0.0
    position_y: float = 0.0
    position_z: float = 0.0
    rotation_x: float = 0.0
    rotation_y: float = 0.0
    rotation_z: float = 0.0


class AssemblyCreate(BaseModel):
    """Schema for creating assembly"""
    name: str = Field(..., description="Assembly name")
    description: Optional[str] = None
    aircraft_type: Optional[str] = None
    is_public: bool = True
    components: List[ComponentPosition] = Field(..., description="Components to assemble")
    auto_align: bool = Field(True, description="Automatically align components")


class InterferenceReport(BaseModel):
    """Schema for interference report"""
    component1: str
    component2: str
    interference_volume_mm3: float
    severity: str  # low, medium, high


class AssemblyValidationResult(BaseModel):
    """Schema for assembly validation"""
    valid: bool
    has_interferences: bool
    interferences: List[InterferenceReport] = []
    warnings: List[str] = []
    errors: List[str] = []
    analysis: Dict[str, Any] = {}


class AssemblyResponse(BaseModel):
    """Schema for assembly response"""
    id: int
    owner_id: int
    name: str
    description: Optional[str] = None
    aircraft_type: Optional[str] = None
    is_public: bool
    assembly_file_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    file_size_mb: float
    is_validated: bool
    has_interferences: bool
    validation_results: Optional[Dict[str, Any]] = None
    component_count: int
    tags: Optional[List[str]] = None
    version: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
