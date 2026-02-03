@echo off
REM Email Notifications Flask Server Startup Script for Windows
REM This script starts the Flask application on port 5002

REM Get the directory where this script is located
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Using venv Python...
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo Using .venv Python...
) else (
    echo No virtual environment found, using system Python...
)

REM Set Python path
set PYTHONPATH=%~dp0;%PYTHONPATH%

REM Start Flask application
echo.
echo ========================================
echo Starting Email Notifications Flask Server
echo Port: 5002
echo Directory: %~dp0
echo Time: %date% %time%
echo ========================================
echo.

REM Run the Flask app
REM Use venv Python if available, otherwise system Python
if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD=venv\Scripts\python.exe
    echo Using venv Python: %PYTHON_CMD%
) else if exist ".venv\Scripts\python.exe" (
    set PYTHON_CMD=.venv\Scripts\python.exe
    echo Using .venv Python: %PYTHON_CMD%
) else (
    set PYTHON_CMD=python
    echo Using system Python: %PYTHON_CMD%
)

echo.
echo Launching Flask app...
echo.
%PYTHON_CMD% app.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo Error: Flask app failed to start
    echo ========================================
    pause
)


