@echo off
REM Create a safe package with sanitized email.json (no real passwords)

echo ========================================
echo Creating SAFE Package (Sanitized)
echo ========================================
echo.
echo This will create a package with example email.json
echo (no real passwords - friend needs to add their own)
echo.

REM First create the regular package
call package_for_sharing.bat

REM Get the package directory (most recent one)
for /f "delims=" %%i in ('dir /b /ad /o-d Email_Notifications_Package_* 2^>nul') do (
    set "PACKAGE_DIR=%%i"
    goto :found
)
:found

if not defined PACKAGE_DIR (
    echo Error: Package directory not found
    pause
    exit /b 1
)

echo.
echo Creating sanitized email.json.example...
echo.

REM Create email.json.example with placeholder data
(
echo {
echo     "example@gmail.com": [
echo         {
echo             "name": "Your Name",
echo             "phone_number": "1234567890",
echo             "smtp_username": "example@gmail.com",
echo             "smtp_password": "YOUR_APP_PASSWORD_HERE",
echo             "years_of_experience": "10+ years",
echo             "linkedin_url": ""
echo         }
echo     ]
echo }
) > "%PACKAGE_DIR%\email.json.example"

REM Remove the real email.json and rename example
if exist "%PACKAGE_DIR%\email.json" (
    echo Removing real email.json (contains sensitive data)...
    del "%PACKAGE_DIR%\email.json"
    echo.
    echo IMPORTANT: Your friend needs to:
    echo   1. Copy email.json.example to email.json
    echo   2. Add their own email credentials
)

echo.
echo ========================================
echo Safe package created!
echo ========================================
echo.
echo Package: %PACKAGE_DIR%
echo.
echo Your friend should:
echo   1. Copy email.json.example to email.json
echo   2. Add their own email credentials to email.json
echo   3. Create .env file from env_example.txt
echo.
pause


