from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import leagues, matches, teams
from app.database import get_db_connection
from app.config import settings
from app.logging_config import logger
import os
import time

# Verificar se a base de dados existe
if not os.path.exists(settings.DATABASE_PATH):
    raise FileNotFoundError(f"Base de dados '{settings.DATABASE_PATH}' não encontrada")

app = FastAPI(
    title="⚽ Football API",
    description="API para consulta de dados das principais ligas europeias de futebol (2023-2024)",
    version=settings.API_VERSION,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log da request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log da response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} | Time: {process_time:.4f}s")
    
    return response

# Tratamento global de exceções
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado: {str(exc)} | URL: {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

# Configurar CORS com configurações de produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],  # Apenas GET pois é read-only
    allow_headers=["*"],
)

# Incluir routers
app.include_router(leagues.router, prefix="/api/v1")
app.include_router(matches.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização"""
    logger.info("🚀 Football API iniciada")
    logger.info(f"Ambiente: {settings.ENVIRONMENT}")
    logger.info(f"Documentação: {'Ativa' if settings.ENABLE_DOCS else 'Desativa'}")

@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "⚽ Football API - Dados das Principais Ligas Europeias",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "season": "2023-2024",
        "leagues": [
            "Premier League (Inglaterra)",
            "La Liga (Espanha)", 
            "Serie A (Itália)",
            "Bundesliga (Alemanha)",
            "Ligue 1 (França)"
        ],
        "endpoints": {
            "docs": settings.docs_url,
            "leagues": "/api/v1/leagues",
            "teams": "/api/v1/teams",
            "matches": "/api/v1/matches"
        }
    }

@app.get("/api/v1/health")
async def health_check():
    """Verificar estado da API e conexão à base de dados"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM leagues")
            leagues_count = cursor.fetchone()[0]
            
        return {
            "status": "healthy",
            "database": "connected",
            "leagues_available": leagues_count,
            "version": settings.API_VERSION,
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        logger.error(f"Health check falhou: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Erro de conexão à base de dados: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level=settings.LOG_LEVEL.lower()
    ) 