"""
FastAPI Main Application
Point d'entrée de l'API Finary Icons
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import icons, generate, health
from app.core.logging import logger

# Créer l'application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API de génération et gestion d'icônes style Finary",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, tags=["health"])
app.include_router(icons.router, prefix="/api", tags=["icons"])
app.include_router(generate.router, prefix="/api", tags=["generate"])

@app.on_event("startup")
async def startup_event():
    """Démarrage de l'application"""
    logger.info(f"🚀 {settings.PROJECT_NAME} starting...")
    logger.info(f"📍 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")

@app.on_event("shutdown")
async def shutdown_event():
    """Arrêt de l'application"""
    logger.info(f"👋 {settings.PROJECT_NAME} shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
