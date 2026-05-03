@echo off
REM Quick Start Script for Quizly Application (Windows)
REM This script starts both backend and frontend servers

echo.
echo ========================================
echo   Quizly Application - Quick Start
echo ========================================
echo.

REM Start Backend
echo Starting Backend Server...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -q -r requirements.txt

echo Seeding database...
python seed_db.py

echo.
echo ========================================
echo Backend starting at http://localhost:8000
echo ========================================
echo.

start "Backend - Quizly" cmd /k "python main.py"

timeout /t 2 /nobreak

REM Start Frontend
cd ..\brainburst-quizzes

echo Starting Frontend Server...

if not exist "node_modules" (
    echo Installing dependencies...
    if command -v bun 2>nul (
        bun install
    ) else (
        npm install
    )
)

echo.
echo ========================================
echo Frontend starting at http://localhost:5173
echo ========================================
echo.
echo Next steps:
echo   1. Open http://localhost:5173 in your browser
echo   2. Open http://localhost:8000/docs for API docs
echo   3. Start taking quizzes!
echo.
echo Press Ctrl+C to stop either server
echo ========================================
echo.

if exist "..\..\..\Users\*\AppData\Local\bun\bin\bun.exe" (
    bun run dev
) else (
    npm run dev
)

pause
