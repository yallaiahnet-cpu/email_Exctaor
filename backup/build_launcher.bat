@echo off
REM Build Flask App Launcher .exe with PyInstaller
echo ========================================
echo Building Flask App Launcher
echo ========================================
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    echo.
)

REM Check if icon file exists
if exist "flask_icon.ico" (
    echo Building with custom icon: flask_icon.ico
    pyinstaller --onefile --windowed --icon=flask_icon.ico --name "Flask App Launcher" launcher.py
) else (
    echo No icon file found. Building without icon...
    echo (To add an icon, save it as 'flask_icon.ico' in this folder)
    pyinstaller --onefile --windowed --name "Flask App Launcher" launcher.py
)

echo.
echo ========================================
if exist "dist\Flask App Launcher.exe" (
    echo Build successful!
    echo.
    echo Your launcher is at: dist\Flask App Launcher.exe
    echo.
    echo You can:
    echo   1. Copy it to your desktop
    echo   2. Double-click to start Flask app
    echo   3. Right-click -^> Properties -^> Change Icon (if needed)
) else (
    echo Build failed. Check the error messages above.
)
echo ========================================
echo.
pause


