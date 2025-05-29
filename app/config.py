import os
from typing import List

class Settings:
    # Configurações da aplicação
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    
    # Base de dados
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "sports_league.sqlite")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Documentação
    ENABLE_DOCS: bool = os.getenv("ENABLE_DOCS", "true").lower() == "true"
    
    # Paginação
    MAX_PAGE_SIZE: int = int(os.getenv("MAX_PAGE_SIZE", "100"))
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def docs_url(self) -> str:
        return "/docs" if self.ENABLE_DOCS else None
    
    @property
    def redoc_url(self) -> str:
        return "/redoc" if self.ENABLE_DOCS else None

settings = Settings() 