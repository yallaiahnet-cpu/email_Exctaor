# Email Notifications Flask Server Startup Script for Windows (PowerShell)
# This script starts the Flask application on port 5002

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Email Notifications Flask Server Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment if it exists
$PythonCmd = $null

if (Test-Path "venv\Scripts\python.exe") {
    Write-Host "Found venv, activating..." -ForegroundColor Green
    & "venv\Scripts\python.exe" --version | Out-Null
    $PythonCmd = "venv\Scripts\python.exe"
    Write-Host "Using venv Python: $PythonCmd" -ForegroundColor Green
}
elseif (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "Found .venv, activating..." -ForegroundColor Green
    & ".venv\Scripts\python.exe" --version | Out-Null
    $PythonCmd = ".venv\Scripts\python.exe"
    Write-Host "Using .venv Python: $PythonCmd" -ForegroundColor Green
}
else {
    Write-Host "No virtual environment found, using system Python..." -ForegroundColor Yellow
    $PythonCmd = "python"
    
    # Check if Python is available
    try {
        $pythonVersion = & python --version 2>&1
        Write-Host "Using system Python: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "Error: Python not found in PATH!" -ForegroundColor Red
        Write-Host "Please install Python or activate a virtual environment." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Set Python path
$env:PYTHONPATH = "$ScriptDir;$env:PYTHONPATH"

# Display startup information
Write-Host ""
Write-Host "Directory: $ScriptDir" -ForegroundColor Gray
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "Port: 5002" -ForegroundColor Gray
Write-Host ""

# Start Flask application
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Launching Flask app..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will be available at: http://localhost:5002" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

try {
    & $PythonCmd app.py
}
catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Error: Flask app failed to start" -ForegroundColor Red
    Write-Host "Error details: $_" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}


