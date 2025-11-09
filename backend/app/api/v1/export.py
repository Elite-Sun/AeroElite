"""Export API Routes"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from pathlib import Path

from app.core.database import get_db
from app.schemas.design import ExportRequest, ExportResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/{design_id}", response_model=ExportResponse)
async def export_design(
    design_id: int,
    export_request: ExportRequest,
    db: AsyncSession = Depends(get_db)
):
    """Export design to specified format"""
    logger.info(f"Exporting design {design_id} to {export_request.format}")

    try:
        from app.models.aircraft import AircraftDesign
        from sqlalchemy import select

        # Get design
        stmt = select(AircraftDesign).where(AircraftDesign.id == design_id)
        result = await db.execute(stmt)
        design = result.scalar_one_or_none()

        if not design:
            raise HTTPException(status_code=404, detail="Design not found")

        # Check if format is supported
        from app.core.config import settings
        if export_request.format.lower() not in settings.SUPPORTED_EXPORT_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported format. Supported: {settings.SUPPORTED_EXPORT_FORMATS}"
            )

        # Get existing file path or generate
        file_path = design.cad_file_path

        if not file_path or not Path(file_path).exists():
            raise HTTPException(status_code=404, detail="CAD file not found")

        # Convert format if needed
        # For now, return existing file
        file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)

        return ExportResponse(
            success=True,
            file_path=file_path,
            download_url=f"/api/v1/export/{design_id}/download",
            file_size_mb=file_size_mb,
            format=export_request.format
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Export error: {e}")
        return ExportResponse(
            success=False,
            format=export_request.format,
            error=str(e)
        )


@router.get("/{design_id}/download")
async def download_design(
    design_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Download exported design file"""
    from app.models.aircraft import AircraftDesign
    from sqlalchemy import select

    stmt = select(AircraftDesign).where(AircraftDesign.id == design_id)
    result = await db.execute(stmt)
    design = result.scalar_one_or_none()

    if not design or not design.cad_file_path:
        raise HTTPException(status_code=404, detail="Design file not found")

    file_path = Path(design.cad_file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=file_path,
        filename=f"{design.name}.{design.cad_format}",
        media_type="application/octet-stream"
    )
