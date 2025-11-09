"""
Assembly Models
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Assembly(Base):
    """Aircraft assembly model"""

    __tablename__ = "assemblies"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic Info
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    aircraft_type = Column(String, nullable=True)  # commercial, fighter, drone, etc.

    # Privacy
    is_public = Column(Boolean, default=True, index=True)

    # Assembly Data
    assembly_file_path = Column(String, nullable=True)
    thumbnail_path = Column(String, nullable=True)
    file_size_mb = Column(Float, default=0.0)

    # Validation
    is_validated = Column(Boolean, default=False)
    has_interferences = Column(Boolean, default=False)
    validation_results = Column(JSON, nullable=True)

    # Metadata
    tags = Column(JSON, nullable=True)
    version = Column(Integer, default=1)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="assemblies")
    components = relationship("AssemblyComponent", back_populates="assembly", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Assembly {self.name}>"


class AssemblyComponent(Base):
    """Components in an assembly"""

    __tablename__ = "assembly_components"

    id = Column(Integer, primary_key=True, index=True)
    assembly_id = Column(Integer, ForeignKey("assemblies.id"), nullable=False)
    design_id = Column(Integer, ForeignKey("aircraft_designs.id"), nullable=False)

    # Component Info
    component_name = Column(String, nullable=False)
    component_role = Column(String, nullable=True)  # primary, secondary, etc.

    # Position & Orientation in Assembly
    position_x = Column(Float, default=0.0)
    position_y = Column(Float, default=0.0)
    position_z = Column(Float, default=0.0)
    rotation_x = Column(Float, default=0.0)
    rotation_y = Column(Float, default=0.0)
    rotation_z = Column(Float, default=0.0)

    # Connection Points
    attachment_points = Column(JSON, nullable=True)  # Connection interfaces

    # Validation
    has_interference = Column(Boolean, default=False)
    interference_volume_mm3 = Column(Float, nullable=True)

    # Relationships
    assembly = relationship("Assembly", back_populates="components")
    design = relationship("AircraftDesign")

    def __repr__(self):
        return f"<AssemblyComponent {self.component_name}>"
