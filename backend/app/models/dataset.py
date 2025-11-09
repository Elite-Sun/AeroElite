"""
Dataset Models for AI Training
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class DatasetEntry(Base):
    """Dataset entry for aircraft designs"""

    __tablename__ = "dataset_entries"

    id = Column(Integer, primary_key=True, index=True)

    # Source Info
    source = Column(String, nullable=False, index=True)  # aircraftverse, grabcad, nasa, etc.
    source_id = Column(String, nullable=True, index=True)
    source_url = Column(String, nullable=True)

    # Design Info
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    aircraft_type = Column(String, nullable=True, index=True)
    component_type = Column(String, nullable=True, index=True)

    # CAD Data
    cad_file_path = Column(String, nullable=True)
    cad_format = Column(String, nullable=True)
    file_size_mb = Column(Float, default=0.0)

    # Extracted Parameters
    parameters = Column(JSON, nullable=True)  # All design parameters

    # Embeddings for AI
    text_embedding = Column(JSON, nullable=True)  # Vector embedding
    parameter_embedding = Column(JSON, nullable=True)

    # Processing Status
    is_processed = Column(Boolean, default=False)
    is_validated = Column(Boolean, default=False)
    processing_errors = Column(Text, nullable=True)

    # Metadata
    tags = Column(JSON, nullable=True)
    license = Column(String, nullable=True)
    author = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<DatasetEntry {self.source}:{self.name}>"


class AirfoilProfile(Base):
    """Airfoil profile data"""

    __tablename__ = "airfoil_profiles"

    id = Column(Integer, primary_key=True, index=True)

    # Airfoil Info
    name = Column(String, unique=True, nullable=False, index=True)
    family = Column(String, nullable=True, index=True)  # NACA, NASA, etc.
    description = Column(Text, nullable=True)

    # Geometric Data
    coordinates = Column(JSON, nullable=False)  # [(x, y), ...]
    num_points = Column(Integer, nullable=False)

    # Performance Characteristics
    max_thickness = Column(Float, nullable=True)  # % chord
    max_camber = Column(Float, nullable=True)  # % chord
    design_cl = Column(Float, nullable=True)  # Design lift coefficient
    design_re = Column(Float, nullable=True)  # Design Reynolds number

    # Aerodynamic Data (if available)
    cl_alpha = Column(Float, nullable=True)  # Lift curve slope
    cl_max = Column(Float, nullable=True)
    cl_min = Column(Float, nullable=True)
    cd_min = Column(Float, nullable=True)
    stall_angle_deg = Column(Float, nullable=True)

    # Source
    source = Column(String, nullable=True)  # g2aero, uiuc, etc.
    source_url = Column(String, nullable=True)

    # Processing
    is_validated = Column(Boolean, default=False)
    embedding = Column(JSON, nullable=True)  # Vector embedding

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<AirfoilProfile {self.name}>"
