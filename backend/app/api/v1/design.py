"""Design API Routes"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from app.core.database import get_db
from app.schemas.design import (
    DesignCreate, DesignResponse, DesignUpdate,
    ValidationResult, ExportRequest, ExportResponse
)
from app.ai.model_manager import ModelManager
from app.cad.generator import CADGenerator
from app.physics.validator import PhysicsValidator

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/create", response_model=DesignResponse)
async def create_design(
    design_data: DesignCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new aircraft design from prompt

    This endpoint:
    1. Parses the natural language prompt
    2. Extracts design parameters using AI
    3. Searches for similar designs in datasets
    4. Generates parametric CAD model
    5. Performs physics validation
    6. Stores in database
    """
    logger.info(f"Creating design from prompt: {design_data.prompt[:100]}...")

    try:
        # Get AI model manager from app state
        model_manager: ModelManager = request.app.state.model_manager

        # Parse prompt to extract parameters
        parsed = await model_manager.parse_prompt(
            design_data.prompt,
            design_data.component_type
        )

        component_type = parsed.get("component_type", design_data.component_type or "unknown")
        parameters = parsed.get("parameters", {})

        # Merge with manual parameters if provided
        if design_data.parameters:
            parameters.update(design_data.parameters)

        # Search for similar designs
        similar_designs = await model_manager.find_similar_designs(parameters)

        # Enhance parameters based on similar designs
        enhanced_parameters = await model_manager.enhance_parameters(
            parameters,
            similar_designs
        )

        # Generate CAD model
        cad_generator = CADGenerator()
        cad_model, metadata = await cad_generator.generate_from_parameters(
            component_type,
            enhanced_parameters
        )

        # Validate design
        physics_validator = PhysicsValidator()
        validation_results = await physics_validator.validate_design(
            component_type,
            enhanced_parameters
        )

        # Generate name if not provided
        design_name = design_data.name or f"{component_type}_{int(time.time())}"

        # Export CAD model temporarily (will move to cloud storage)
        import tempfile
        from pathlib import Path
        import time

        temp_dir = Path(tempfile.gettempdir()) / "aeroelite" / "models"
        temp_dir.mkdir(parents=True, exist_ok=True)
        output_file = temp_dir / f"{design_name}.step"

        exported_path = await cad_generator.export_model(
            cad_model,
            output_file,
            format="step"
        )

        # Calculate file size
        file_size_mb = exported_path.stat().st_size / (1024 * 1024)

        # Create database entry
        from app.models.aircraft import AircraftDesign
        from sqlalchemy import insert

        design_dict = {
            "owner_id": 1,  # TODO: Get from auth
            "name": design_name,
            "description": design_data.prompt,
            "component_type": component_type,
            "prompt": design_data.prompt,
            "ai_model_version": "gemini-1.5-pro",
            "is_public": design_data.is_public,
            "allow_learning": design_data.allow_learning,
            "cad_file_path": str(exported_path),
            "cad_format": "step",
            "file_size_mb": file_size_mb,
            "parameters": enhanced_parameters,
            "is_validated": validation_results["valid"],
            "validation_results": validation_results,
            "tags": [component_type],
            "version": 1,
        }

        stmt = insert(AircraftDesign).values(**design_dict).returning(AircraftDesign)
        result = await db.execute(stmt)
        design = result.scalar_one()
        await db.commit()
        await db.refresh(design)

        logger.info(f"Design created successfully: {design.id}")

        return design

    except Exception as e:
        logger.error(f"Error creating design: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{design_id}", response_model=DesignResponse)
async def get_design(
    design_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get design by ID"""
    from app.models.aircraft import AircraftDesign
    from sqlalchemy import select

    stmt = select(AircraftDesign).where(AircraftDesign.id == design_id)
    result = await db.execute(stmt)
    design = result.scalar_one_or_none()

    if not design:
        raise HTTPException(status_code=404, detail="Design not found")

    return design


@router.put("/{design_id}", response_model=DesignResponse)
async def update_design(
    design_id: int,
    update_data: DesignUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update design parameters"""
    from app.models.aircraft import AircraftDesign
    from sqlalchemy import select, update

    # Get existing design
    stmt = select(AircraftDesign).where(AircraftDesign.id == design_id)
    result = await db.execute(stmt)
    design = result.scalar_one_or_none()

    if not design:
        raise HTTPException(status_code=404, detail="Design not found")

    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)

    if update_dict:
        stmt = (
            update(AircraftDesign)
            .where(AircraftDesign.id == design_id)
            .values(**update_dict)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(design)

    return design


@router.post("/{design_id}/validate", response_model=ValidationResult)
async def validate_design(
    design_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Run physics validation on design"""
    from app.models.aircraft import AircraftDesign
    from sqlalchemy import select

    stmt = select(AircraftDesign).where(AircraftDesign.id == design_id)
    result = await db.execute(stmt)
    design = result.scalar_one_or_none()

    if not design:
        raise HTTPException(status_code=404, detail="Design not found")

    # Run validation
    validator = PhysicsValidator()
    results = await validator.validate_design(
        design.component_type,
        design.parameters or {}
    )

    # Update design validation status
    from sqlalchemy import update
    stmt = (
        update(AircraftDesign)
        .where(AircraftDesign.id == design_id)
        .values(
            is_validated=results["valid"],
            validation_results=results
        )
    )
    await db.execute(stmt)
    await db.commit()

    return results


@router.get("/", response_model=List[DesignResponse])
async def list_designs(
    skip: int = 0,
    limit: int = 20,
    component_type: Optional[str] = None,
    public_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """List designs with filtering"""
    from app.models.aircraft import AircraftDesign
    from sqlalchemy import select

    stmt = select(AircraftDesign).offset(skip).limit(limit)

    if public_only:
        stmt = stmt.where(AircraftDesign.is_public == True)

    if component_type:
        stmt = stmt.where(AircraftDesign.component_type == component_type)

    stmt = stmt.order_by(AircraftDesign.created_at.desc())

    result = await db.execute(stmt)
    designs = result.scalars().all()

    return designs


@router.delete("/{design_id}")
async def delete_design(
    design_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete design"""
    from app.models.aircraft import AircraftDesign
    from sqlalchemy import delete

    stmt = delete(AircraftDesign).where(AircraftDesign.id == design_id)
    result = await db.execute(stmt)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Design not found")

    return {"success": True, "message": "Design deleted"}
