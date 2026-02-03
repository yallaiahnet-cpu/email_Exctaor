@echo off
REM Package Email Notifications project for sharing
REM This creates a clean package without unnecessary files

echo ========================================
echo Packaging Email Notifications Project
echo ========================================
echo.

REM Get the current directory name
for %%I in ("%CD%") do set "FOLDER_NAME=%%~nxI"

REM Create package directory
set "PACKAGE_NAME=Email_Notifications_Package"
set "PACKAGE_DIR=%PACKAGE_NAME%_%date:~-4,4%%date:~-7,2%%date:~-10,2%"

echo Creating package directory: %PACKAGE_DIR%
if exist "%PACKAGE_DIR%" (
    echo Removing existing package directory...
    rmdir /s /q "%PACKAGE_DIR%"
)
mkdir "%PACKAGE_DIR%"

echo.
echo Copying essential files...
echo.

REM Copy essential Python files
echo [1/8] Copying Python files...
copy /Y "app.py" "%PACKAGE_DIR%\" >nul
copy /Y "cleaning_jd.py" "%PACKAGE_DIR%\" >nul
copy /Y "send_email.py" "%PACKAGE_DIR%\" >nul
copy /Y "llm_exctration.py" "%PACKAGE_DIR%\" >nul
copy /Y "document_creation.py" "%PACKAGE_DIR%\" >nul
copy /Y "job_scraper.py" "%PACKAGE_DIR%\" >nul
if exist "launcher.py" copy /Y "launcher.py" "%PACKAGE_DIR%\" >nul

REM Copy requirements and config files
echo [2/8] Copying configuration files...
copy /Y "requirements.txt" "%PACKAGE_DIR%\" >nul
copy /Y "Procfile" "%PACKAGE_DIR%\" >nul 2>nul
copy /Y "render.yaml" "%PACKAGE_DIR%\" >nul 2>nul
copy /Y ".gitignore" "%PACKAGE_DIR%\" >nul
copy /Y "env_example.txt" "%PACKAGE_DIR%\" >nul

REM Copy templates directory
echo [3/8] Copying templates...
xcopy /E /I /Y "templates" "%PACKAGE_DIR%\templates" >nul

REM Copy essential JSON data files
echo [4/8] Copying data files...
if exist "email.json" copy /Y "email.json" "%PACKAGE_DIR%\" >nul
if exist "otter_links.json" copy /Y "otter_links.json" "%PACKAGE_DIR%\" >nul
if exist "sent_emails.json" copy /Y "sent_emails.json" "%PACKAGE_DIR%\" >nul
if exist "bold_words.json" copy /Y "bold_words.json" "%PACKAGE_DIR%\" >nul
if exist "nvoids_jobs.json" copy /Y "nvoids_jobs.json" "%PACKAGE_DIR%\" >nul
if exist "resunedotnet.json" copy /Y "resunedotnet.json" "%PACKAGE_DIR%\" >nul
if exist "senior_aws_data_engineer_resume.json" copy /Y "senior_aws_data_engineer_resume.json" "%PACKAGE_DIR%\" >nul

REM Copy Windows start scripts
echo [5/8] Copying Windows scripts...
if exist "start_flask.bat" copy /Y "start_flask.bat" "%PACKAGE_DIR%\" >nul
if exist "start_flask_simple.bat" copy /Y "start_flask_simple.bat" "%PACKAGE_DIR%\" >nul
if exist "start_flask.ps1" copy /Y "start_flask.ps1" "%PACKAGE_DIR%\" >nul
if exist "start_flask.vbs" copy /Y "start_flask.vbs" "%PACKAGE_DIR%\" >nul
if exist "start_flask_silent.vbs" copy /Y "start_flask_silent.vbs" "%PACKAGE_DIR%\" >nul
if exist "create_shortcut.vbs" copy /Y "create_shortcut.vbs" "%PACKAGE_DIR%\" >nul
if exist "build_launcher.bat" copy /Y "build_launcher.bat" "%PACKAGE_DIR%\" >nul

REM Copy Mac/Linux start scripts
echo [6/8] Copying Mac/Linux scripts...
if exist "run_flask.sh" copy /Y "run_flask.sh" "%PACKAGE_DIR%\" >nul
if exist "start_server.sh" copy /Y "start_server.sh" "%PACKAGE_DIR%\" >nul
if exist "cleanup_for_deployment.sh" copy /Y "cleanup_for_deployment.sh" "%PACKAGE_DIR%\" >nul

REM Copy documentation
echo [7/8] Copying documentation...
if exist "README.md" copy /Y "README.md" "%PACKAGE_DIR%\" >nul
if exist "WINDOWS_SETUP.md" copy /Y "WINDOWS_SETUP.md" "%PACKAGE_DIR%\" >nul
if exist "QUICK_START_ICON.md" copy /Y "QUICK_START_ICON.md" "%PACKAGE_DIR%\" >nul
if exist "CREATE_ICON_SHORTCUT.md" copy /Y "CREATE_ICON_SHORTCUT.md" "%PACKAGE_DIR%\" >nul
if exist "RENDER_DEPLOYMENT.md" copy /Y "RENDER_DEPLOYMENT.md" "%PACKAGE_DIR%\" >nul
if exist "DEPLOYMENT_CHECKLIST.md" copy /Y "DEPLOYMENT_CHECKLIST.md" "%PACKAGE_DIR%\" >nul
if exist "BUILD_EXE_LAUNCHER.md" copy /Y "BUILD_EXE_LAUNCHER.md" "%PACKAGE_DIR%\" >nul

REM Create empty directories that might be needed
echo [8/8] Creating necessary directories...
if not exist "%PACKAGE_DIR%\resumes" mkdir "%PACKAGE_DIR%\resumes"
if not exist "%PACKAGE_DIR%\generated_resumes" mkdir "%PACKAGE_DIR%\generated_resumes"

REM Create a README for the friend
echo Creating README for recipient...
(
echo # Email Notifications Flask Application
echo.
echo ## Quick Start
echo.
echo ### Windows:
echo 1. Install Python 3.8+ from https://www.python.org/downloads/
echo 2. Open Command Prompt in this folder
echo 3. Run: `pip install -r requirements.txt`
echo 4. Copy `env_example.txt` to `.env` and add your GROQ_API_KEY
echo 5. Double-click `start_flask_simple.bat` to start
echo.
echo ### Mac/Linux:
echo 1. Install Python 3.8+
echo 2. Run: `pip install -r requirements.txt`
echo 3. Copy `env_example.txt` to `.env` and add your GROQ_API_KEY
echo 4. Run: `python app.py`
echo.
echo ## Configuration
echo.
echo 1. Copy `env_example.txt` to `.env`
echo 2. Add your GROQ_API_KEY in `.env` file
echo 3. Update `email.json` with your email credentials if needed
echo.
echo ## Documentation
echo.
echo - `WINDOWS_SETUP.md` - Detailed Windows setup guide
echo - `QUICK_START_ICON.md` - Create desktop shortcut
echo - `RENDER_DEPLOYMENT.md` - Deploy to Render cloud
echo.
echo ## Support
echo.
echo If you encounter issues, check the documentation files or contact the sender.
) > "%PACKAGE_DIR%\README_FOR_FRIEND.md"

echo.
echo ========================================
echo Package created successfully!
echo ========================================
echo.
echo Package location: %PACKAGE_DIR%
echo.
echo Next steps:
echo 1. Review the package folder
echo 2. Create a ZIP file: Right-click folder -^> Send to -^> Compressed folder
echo 3. Share the ZIP file with your friend
echo.
echo IMPORTANT: Make sure email.json doesn't contain sensitive data
echo            or inform your friend to update it with their own credentials.
echo.
pause


