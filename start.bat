@echo off
echo.
echo ======================================
echo    ⚽ Football API + MCP Server
echo ======================================
echo.
echo 🚀 Starting server...
echo.
echo Available APIs:
echo   📊 REST API: http://localhost:8000
echo   📚 Docs: http://localhost:8000/docs
echo   🤖 MCP Server: http://localhost:8000/mcp
echo.
echo To configure MCP in Cursor:
echo   Location: ~/.cursor/mcp.json
echo   See: MCP_SETUP.md for details
echo.
echo ======================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if database exists
if not exist "sports_league.sqlite" (
    echo ❌ ERROR: Database 'sports_league.sqlite' not found!
    echo.
    pause
    exit /b 1
)

REM Start server
echo 🏃 Running uvicorn...
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 