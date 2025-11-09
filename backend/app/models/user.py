"""
User Model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    """User model for authentication and profile"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    full_name = Column(String, nullable=True)

    # OAuth
    google_id = Column(String, unique=True, nullable=True, index=True)
    oauth_provider = Column(String, nullable=True)

    # Account Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Usage & Billing
    storage_used_mb = Column(Float, default=0.0)
    design_count = Column(Integer, default=0)
    public_design_count = Column(Integer, default=0)
    private_design_count = Column(Integer, default=0)

    # Preferences
    theme = Column(String, default="light")  # light or dark
    default_privacy = Column(String, default="public")  # public or private

    # Relationships
    designs = relationship("AircraftDesign", back_populates="owner", cascade="all, delete-orphan")
    assemblies = relationship("Assembly", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
