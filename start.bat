@echo off
echo ===================================
echo   ⚽ Football API - Inicializacao 
echo ===================================
echo.

REM Verificar se o ambiente virtual existe
if not exist "venv\" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    echo ✅ Ambiente virtual criado!
    echo.
)

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate
echo ✅ Ambiente virtual ativado!
echo.

REM Instalar dependências
echo 📚 Instalando dependências...
pip install -r requirements.txt --quiet
echo ✅ Dependências instaladas!
echo.

REM Verificar se a base de dados existe
if not exist "sports_league.sqlite" (
    echo ❌ ERRO: Base de dados 'sports_league.sqlite' não encontrada!
    echo    Por favor, coloque o ficheiro na raiz do projeto.
    pause
    exit /b 1
)

echo 🚀 Iniciando a API...
echo.
echo 📱 Aceder em: http://localhost:8000
echo 📖 Documentação: http://localhost:8000/docs
echo.
echo ⌨️  Pressione Ctrl+C para parar a API
echo.

uvicorn app.main:app --reload 