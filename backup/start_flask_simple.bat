@echo off
REM Simple Flask Startup Script for Windows
REM Quick start without virtual environment checks

cd /d "%~dp0"

echo Starting Flask app on port 5002...
echo.

REM Try venv first, then system Python
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe app.py
) else if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe app.py
) else (
    python app.py
)

pause


