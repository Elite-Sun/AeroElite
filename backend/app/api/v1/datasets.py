"""Datasets API Routes"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict, Any, Optional
import logging

from app.services.dataset_service import DatasetService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list")
async def list_datasets(
    request: Request
):
    """List available datasets"""
    dataset_service: DatasetService = request.app.state.dataset_service

    return {
        "datasets": dataset_service.datasets,
        "total_count": sum(ds["total_entries"] for ds in dataset_service.datasets.values())
    }


@router.post("/download/{dataset_name}")
async def download_dataset(
    dataset_name: str,
    force: bool = False,
    request: Request = None
):
    """Download dataset"""
    logger.info(f"Downloading dataset: {dataset_name}")

    dataset_service = DatasetService()
    result = await dataset_service.download_dataset(dataset_name, force=force)

    return result


@router.get("/search")
async def search_datasets(
    query: str,
    dataset: Optional[str] = None,
    limit: int = 10,
    request: Request = None
):
    """Search datasets"""
    dataset_service = DatasetService()
    results = await dataset_service.search_datasets(query, dataset)

    return {
        "query": query,
        "results": results[:limit],
        "total_found": len(results)
    }


@router.get("/airfoils")
async def list_airfoils(
    family: Optional[str] = None,
    limit: int = 50
):
    """List airfoil profiles"""
    # Would query airfoil database
    sample_airfoils = [
        {"name": "NACA2412", "family": "NACA 4-digit"},
        {"name": "NACA0012", "family": "NACA 4-digit"},
        {"name": "NACA23012", "family": "NACA 5-digit"},
    ]

    return {
        "airfoils": sample_airfoils,
        "total": len(sample_airfoils)
    }
