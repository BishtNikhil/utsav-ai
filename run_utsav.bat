@echo off
title UtsavAI - Autonomous Celebration & Event Orchestrator
color 0B
echo ======================================================================
echo    UTSAV AI : AUTONOMOUS CELEBRATION & EVENT ORCHESTRATOR
echo    PromptWars Virtual 2026 - Main Challenge 05
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b 1
)

echo [2/3] Checking dependencies...
python -c "import fastapi, uvicorn" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
)

echo [3/3] Starting UtsavAI Server on http://localhost:8080 ...
start "" http://localhost:8080
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
pause
