"""
Main FastAPI application for Numerology Chat App.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from pathlib import Path

from app.api.endpoints import router
from app.core.config import settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title="Numerology Chat API",
        description="API for numerology calculations and chat interactions",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add trusted host middleware (optional, for security)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # In production, specify actual hosts
    )
    
    # Include routers
    app.include_router(router, prefix="/api/v1")
    
    # Mount Sphinx documentation
    sphinx_docs_path = Path(__file__).parent.parent.parent / "docs" / "sphinx" / "_build" / "html"
    if sphinx_docs_path.exists():
        app.mount("/sphinx-docs", StaticFiles(directory=str(sphinx_docs_path), html=True), name="sphinx-docs")
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Numerology Chat API",
            "version": "1.0.0",
            "docs": "/docs",
            "sphinx_docs": "/sphinx-docs",
            "status": "running"
        }
    
    # Health check endpoint
    @app.get("/health")
    async def health():
        return {"status": "healthy", "message": "Service is running"}
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=True
    )