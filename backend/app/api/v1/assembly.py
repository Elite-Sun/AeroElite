"""Assembly API Routes"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.core.database import get_db
from app.schemas.assembly import AssemblyCreate, AssemblyResponse, AssemblyValidationResult
from app.assembly.assembler import Assembler
from app.physics.validator import PhysicsValidator

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/create", response_model=AssemblyResponse)
async def create_assembly(
    assembly_data: AssemblyCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create aircraft assembly from components"""
    logger.info(f"Creating assembly: {assembly_data.name}")

    try:
        # Load component designs
        from app.models.aircraft import AircraftDesign
        from sqlalchemy import select

        components = []
        for comp_pos in assembly_data.components:
            stmt = select(AircraftDesign).where(AircraftDesign.id == comp_pos.design_id)
            result = await db.execute(stmt)
            design = result.scalar_one_or_none()

            if not design:
                raise HTTPException(
                    status_code=404,
                    detail=f"Design {comp_pos.design_id} not found"
                )

            # Load CAD model (simplified for demo)
            components.append({
                "design_id": design.id,
                "component_type": design.component_type,
                "parameters": design.parameters,
                "model": None,  # Would load actual CAD model here
                "position": comp_pos
            })

        # Create assembly
        assembler = Assembler()
        # assembly_model, results = await assembler.create_assembly(components)

        # For now, create database entry
        from app.models.assembly import Assembly
        from sqlalchemy import insert

        assembly_dict = {
            "owner_id": 1,  # TODO: Get from auth
            "name": assembly_data.name,
            "description": assembly_data.description,
            "aircraft_type": assembly_data.aircraft_type,
            "is_public": assembly_data.is_public,
            "is_validated": False,
            "has_interferences": False,
        }

        stmt = insert(Assembly).values(**assembly_dict).returning(Assembly)
        result = await db.execute(stmt)
        assembly = result.scalar_one()

        # Add components
        from app.models.assembly import AssemblyComponent

        for comp_pos in assembly_data.components:
            comp_dict = {
                "assembly_id": assembly.id,
                "design_id": comp_pos.design_id,
                "component_name": comp_pos.component_name,
                "position_x": comp_pos.position_x,
                "position_y": comp_pos.position_y,
                "position_z": comp_pos.position_z,
                "rotation_x": comp_pos.rotation_x,
                "rotation_y": comp_pos.rotation_y,
                "rotation_z": comp_pos.rotation_z,
            }
            stmt = insert(AssemblyComponent).values(**comp_dict)
            await db.execute(stmt)

        await db.commit()
        await db.refresh(assembly)

        logger.info(f"Assembly created: {assembly.id}")
        return assembly

    except Exception as e:
        logger.error(f"Error creating assembly: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{assembly_id}", response_model=AssemblyResponse)
async def get_assembly(
    assembly_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get assembly by ID"""
    from app.models.assembly import Assembly
    from sqlalchemy import select

    stmt = select(Assembly).where(Assembly.id == assembly_id)
    result = await db.execute(stmt)
    assembly = result.scalar_one_or_none()

    if not assembly:
        raise HTTPException(status_code=404, detail="Assembly not found")

    return assembly


@router.post("/{assembly_id}/validate", response_model=AssemblyValidationResult)
async def validate_assembly(
    assembly_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Validate assembly for interferences and physics"""
    from app.models.assembly import Assembly, AssemblyComponent
    from sqlalchemy import select

    stmt = select(Assembly).where(Assembly.id == assembly_id)
    result = await db.execute(stmt)
    assembly = result.scalar_one_or_none()

    if not assembly:
        raise HTTPException(status_code=404, detail="Assembly not found")

    # Get components
    stmt = select(AssemblyComponent).where(AssemblyComponent.assembly_id == assembly_id)
    result = await db.execute(stmt)
    components = result.scalars().all()

    # Run validation
    validator = PhysicsValidator()
    # Convert to format expected by validator
    component_data = [{"component_type": "wing"}]  # Simplified

    results = await validator.validate_assembly(component_data)

    return results


@router.get("/", response_model=List[AssemblyResponse])
async def list_assemblies(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """List assemblies"""
    from app.models.assembly import Assembly
    from sqlalchemy import select

    stmt = (
        select(Assembly)
        .where(Assembly.is_public == True)
        .offset(skip)
        .limit(limit)
        .order_by(Assembly.created_at.desc())
    )

    result = await db.execute(stmt)
    assemblies = result.scalars().all()
    return assemblies
