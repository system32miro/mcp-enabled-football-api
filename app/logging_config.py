import logging
import sys
from datetime import datetime
from app.config import settings

def setup_logging():
    """Configurar logging para a aplicação"""
    
    # Formato para logs
    log_format = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    
    # Configurar o logger principal
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f"api_{datetime.now().strftime('%Y%m%d')}.log")
        ]
    )
    
    # Logger específico para a aplicação
    logger = logging.getLogger("football_api")
    
    # Em produção, desabilitar logs de debug do uvicorn
    if settings.is_production:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    return logger

# Criar logger global
logger = setup_logging() 