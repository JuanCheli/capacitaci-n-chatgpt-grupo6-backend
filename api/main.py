from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config.config import settings
from .routes.simulador_router import router as simulador_router


def create_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI"""
    app = FastAPI(
        title=settings.APP_NAME,
        description="API para simular ChatGPT y sistema RAG para capacitación",
        version="1.0.0"
    )

    # Configurar CORS - permite todas las origins para demo/capacitación
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Incluir routers
    app.include_router(simulador_router)

    @app.get("/")
    async def root():
        """Endpoint de bienvenida"""
        return {
            "message": "Bienvenido al Simulador ChatGPT para Capacitación",
            "endpoints": {
                "simulador_chat": "/simulador/chat",
                "simulador_rag": "/simulador/rag",
                "docs": "/docs"
            }
        }

    @app.get("/health")
    async def health_check():
        """Verificar estado del servicio"""
        return {
            "status": "healthy",
            "app_name": settings.APP_NAME,
            "model": settings.GEMINI_MODEL,
            "api_configured": settings.GEMINI_API_KEY is not None
        }

    return app


app = create_app()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"🚀 Iniciando {settings.APP_NAME}")
logger.info(f"📝 Modelo configurado: {settings.GEMINI_MODEL}")
logger.info(f"🔑 API Key configurada: {'Sí' if settings.GEMINI_API_KEY else 'No (modo simulación)'}")
