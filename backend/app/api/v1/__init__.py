"""API v1 Router"""

from fastapi import APIRouter
from app.api.v1 import design, assembly, auth, datasets, export

api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(design.router, prefix="/design", tags=["Design"])
api_router.include_router(assembly.router, prefix="/assembly", tags=["Assembly"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
api_router.include_router(export.router, prefix="/export", tags=["Export"])
