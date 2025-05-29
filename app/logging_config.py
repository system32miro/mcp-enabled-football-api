import logging
import sys
from datetime import datetime
from app.config import settings

def setup_logging():
    """Configurar logging para a aplicação"""
    
    # Formato para logs (sem emojis para compatibilidade Windows)
    log_format = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    
    # Configurar handlers com codificação UTF-8
    handlers = []
    
    # Console handler com codificação UTF-8
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    if hasattr(console_handler.stream, 'reconfigure'):
        # Python 3.7+ - configurar para UTF-8
        try:
            console_handler.stream.reconfigure(encoding='utf-8')
        except Exception:
            pass  # Se falhar, continua com a codificação padrão
    handlers.append(console_handler)
    
    # File handler com codificação UTF-8
    try:
        file_handler = logging.FileHandler(
            f"api_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    except Exception:
        # Se falhar a criar o ficheiro, continua apenas com console
        pass
    
    # Configurar o logger principal
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=log_format,
        handlers=handlers,
        force=True  # Substitui configuração existente
    )
    
    # Logger específico para a aplicação
    logger = logging.getLogger("football_api")
    
    # Em produção, desabilitar logs de debug do uvicorn
    if settings.is_production:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    return logger

# Criar logger global
logger = setup_logging() 