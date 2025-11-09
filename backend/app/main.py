"""
Main FastAPI Application
Aero Elite - AI-Assisted 3D Aircraft Design System
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import api_router
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("Starting Aero Elite Backend...")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Initialize AI models
    try:
        from app.ai.model_manager import ModelManager
        model_manager = ModelManager()
        await model_manager.initialize()
        app.state.model_manager = model_manager
        logger.info("AI models loaded successfully")
    except Exception as e:
        logger.error(f"Error loading AI models: {e}")

    # Initialize dataset cache
    try:
        from app.services.dataset_service import DatasetService
        dataset_service = DatasetService()
        await dataset_service.load_metadata()
        app.state.dataset_service = dataset_service
        logger.info("Dataset metadata loaded")
    except Exception as e:
        logger.error(f"Error loading datasets: {e}")

    yield

    # Cleanup
    logger.info("Shutting down Aero Elite Backend...")


# Create FastAPI app
app = FastAPI(
    title="Aero Elite API",
    description="AI-Assisted 3D Aircraft Design System",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    # Process request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)

        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} Time: {process_time:.3f}s"
        )

        return response
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url.path} Error: {str(e)}")
        raise


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Aero Elite Backend"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Aero Elite API",
        "version": "1.0.0",
        "description": "AI-Assisted 3D Aircraft Design System",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Include API router
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
