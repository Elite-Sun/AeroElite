"""
Aircraft Design Models
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class AircraftDesign(Base):
    """Aircraft design/component model"""

    __tablename__ = "aircraft_designs"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic Info
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    component_type = Column(String, nullable=False, index=True)  # wing, fuselage, tail, etc.

    # Design Source
    prompt = Column(Text, nullable=True)  # Original user prompt
    ai_model_version = Column(String, nullable=True)  # AI model used
    based_on_design_id = Column(Integer, ForeignKey("aircraft_designs.id"), nullable=True)

    # Privacy
    is_public = Column(Boolean, default=True, index=True)
    allow_learning = Column(Boolean, default=True)  # Allow AI to learn from this

    # CAD Data
    cad_file_path = Column(String, nullable=True)  # Cloud storage path
    cad_format = Column(String, nullable=True)  # step, iges, etc.
    thumbnail_path = Column(String, nullable=True)
    file_size_mb = Column(Float, default=0.0)

    # Parametric Data (JSON)
    parameters = Column(JSON, nullable=True)  # All design parameters

    # Physics Validation
    is_validated = Column(Boolean, default=False)
    validation_results = Column(JSON, nullable=True)
    validation_warnings = Column(JSON, nullable=True)

    # Metadata
    tags = Column(JSON, nullable=True)  # Searchable tags
    version = Column(Integer, default=1)
    downloads = Column(Integer, default=0)
    likes = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="designs")
    components = relationship("Component", back_populates="design", cascade="all, delete-orphan")
    design_parameters = relationship("Parameter", back_populates="design", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AircraftDesign {self.name} ({self.component_type})>"


class Component(Base):
    """Sub-components of a design"""

    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    design_id = Column(Integer, ForeignKey("aircraft_designs.id"), nullable=False)

    # Component Info
    name = Column(String, nullable=False)
    component_type = Column(String, nullable=False)  # spar, rib, skin, etc.
    parent_component_id = Column(Integer, ForeignKey("components.id"), nullable=True)

    # Geometry
    geometry_data = Column(JSON, nullable=True)  # Geometric parameters
    material = Column(String, nullable=True)
    weight_kg = Column(Float, nullable=True)

    # Position & Orientation
    position_x = Column(Float, default=0.0)
    position_y = Column(Float, default=0.0)
    position_z = Column(Float, default=0.0)
    rotation_x = Column(Float, default=0.0)
    rotation_y = Column(Float, default=0.0)
    rotation_z = Column(Float, default=0.0)

    # Relationships
    design = relationship("AircraftDesign", back_populates="components")
    children = relationship("Component", backref="parent", remote_side=[id])

    def __repr__(self):
        return f"<Component {self.name} ({self.component_type})>"


class Parameter(Base):
    """Design parameters for parametric modeling"""

    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True)
    design_id = Column(Integer, ForeignKey("aircraft_designs.id"), nullable=False)

    # Parameter Info
    name = Column(String, nullable=False, index=True)
    display_name = Column(String, nullable=True)
    parameter_type = Column(String, nullable=False)  # dimension, angle, count, material, etc.
    unit = Column(String, nullable=True)  # m, deg, kg, etc.

    # Value
    value = Column(Float, nullable=True)
    value_string = Column(String, nullable=True)  # For non-numeric values

    # Constraints
    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)
    allowed_values = Column(JSON, nullable=True)  # For discrete choices

    # Metadata
    description = Column(Text, nullable=True)
    is_editable = Column(Boolean, default=True)
    is_key_parameter = Column(Boolean, default=False)  # Important for AI learning

    # Relationships
    design = relationship("AircraftDesign", back_populates="design_parameters")

    def __repr__(self):
        return f"<Parameter {self.name}={self.value}>"
