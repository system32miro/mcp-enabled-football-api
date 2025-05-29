# Usar Python 3.11 slim para imagem mais leve
FROM python:3.11-slim

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash apiuser

# Definir diretório de trabalho
WORKDIR /app

# Copiar ficheiros de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app/ ./app/

# Copiar base de dados
COPY sports_league.sqlite .

# Criar diretório para logs
RUN mkdir -p /app/logs

# Mudar proprietário dos ficheiros para o usuário não-root
RUN chown -R apiuser:apiuser /app

# Mudar para usuário não-root
USER apiuser

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"] 