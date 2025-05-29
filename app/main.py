from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP
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
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log apenas em desenvolvimento ou requests com erro
    if not settings.is_production or response.status_code >= 400:
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.4f}s"
        )
    
    return response

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],  # Apenas GET para segurança
    allow_headers=["*"],
)

# Tratamento global de erros
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor. Contacte o administrador."}
    )

# Incluir routers
app.include_router(leagues.router, prefix="/api/v1", tags=["leagues"])
app.include_router(matches.router, prefix="/api/v1", tags=["matches"])
app.include_router(teams.router, prefix="/api/v1", tags=["teams"])

# Endpoint de health check
@app.get("/api/v1/health", operation_id="health_check")
async def health_check():
    """Verificar estado da API e conectividade da base de dados"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM leagues")
        league_count = cursor.fetchone()[0]
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "leagues_available": league_count,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Health check falhou: {e}")
        raise HTTPException(status_code=503, detail="Base de dados indisponível")

# Criar e configurar MCP Server
mcp = FastApiMCP(
    app,
    name="Football Data MCP",
    description="MCP server para consulta de dados de futebol das principais ligas europeias (2023-2024). Fornece informações sobre equipas, jogadores, jogos, classificações e estatísticas das 5 principais ligas: Premier League, La Liga, Serie A, Bundesliga e Ligue 1.",
    # Incluir todas as respostas possíveis nas descrições das tools
    describe_all_responses=True,
    # Incluir schema JSON completo para melhor compreensão dos agentes
    describe_full_response_schema=True
)

# Montar o MCP server na aplicação
mcp.mount()

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização"""
    logger.info("Football API iniciada com sucesso")
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
            "matches": "/api/v1/matches",
            "mcp": "/mcp"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level=settings.LOG_LEVEL.lower()
    ) 