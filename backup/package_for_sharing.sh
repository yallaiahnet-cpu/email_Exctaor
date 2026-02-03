#!/bin/bash

# Package Email Notifications project for sharing
# This creates a clean package without unnecessary files

echo "========================================"
echo "Packaging Email Notifications Project"
echo "========================================"
echo ""

# Get current directory name
FOLDER_NAME=$(basename "$PWD")

# Create package directory with date
PACKAGE_NAME="Email_Notifications_Package"
DATE_SUFFIX=$(date +%Y%m%d)
PACKAGE_DIR="${PACKAGE_NAME}_${DATE_SUFFIX}"

echo "Creating package directory: $PACKAGE_DIR"
if [ -d "$PACKAGE_DIR" ]; then
    echo "Removing existing package directory..."
    rm -rf "$PACKAGE_DIR"
fi
mkdir -p "$PACKAGE_DIR"

echo ""
echo "Copying essential files..."
echo ""

# Copy essential Python files
echo "[1/8] Copying Python files..."
cp -f app.py "$PACKAGE_DIR/" 2>/dev/null
cp -f cleaning_jd.py "$PACKAGE_DIR/" 2>/dev/null
cp -f send_email.py "$PACKAGE_DIR/" 2>/dev/null
cp -f llm_exctration.py "$PACKAGE_DIR/" 2>/dev/null
cp -f document_creation.py "$PACKAGE_DIR/" 2>/dev/null
cp -f job_scraper.py "$PACKAGE_DIR/" 2>/dev/null
[ -f launcher.py ] && cp -f launcher.py "$PACKAGE_DIR/" 2>/dev/null

# Copy requirements and config files
echo "[2/8] Copying configuration files..."
cp -f requirements.txt "$PACKAGE_DIR/" 2>/dev/null
cp -f Procfile "$PACKAGE_DIR/" 2>/dev/null
cp -f render.yaml "$PACKAGE_DIR/" 2>/dev/null
cp -f .gitignore "$PACKAGE_DIR/" 2>/dev/null
cp -f env_example.txt "$PACKAGE_DIR/" 2>/dev/null

# Copy templates directory
echo "[3/8] Copying templates..."
if [ -d "templates" ]; then
    cp -r templates "$PACKAGE_DIR/" 2>/dev/null
fi

# Copy essential JSON data files
echo "[4/8] Copying data files..."
[ -f email.json ] && cp -f email.json "$PACKAGE_DIR/" 2>/dev/null
[ -f otter_links.json ] && cp -f otter_links.json "$PACKAGE_DIR/" 2>/dev/null
[ -f sent_emails.json ] && cp -f sent_emails.json "$PACKAGE_DIR/" 2>/dev/null
[ -f bold_words.json ] && cp -f bold_words.json "$PACKAGE_DIR/" 2>/dev/null
[ -f nvoids_jobs.json ] && cp -f nvoids_jobs.json "$PACKAGE_DIR/" 2>/dev/null
[ -f resunedotnet.json ] && cp -f resunedotnet.json "$PACKAGE_DIR/" 2>/dev/null
[ -f senior_aws_data_engineer_resume.json ] && cp -f senior_aws_data_engineer_resume.json "$PACKAGE_DIR/" 2>/dev/null

# Copy Windows start scripts
echo "[5/8] Copying Windows scripts..."
[ -f start_flask.bat ] && cp -f start_flask.bat "$PACKAGE_DIR/" 2>/dev/null
[ -f start_flask_simple.bat ] && cp -f start_flask_simple.bat "$PACKAGE_DIR/" 2>/dev/null
[ -f start_flask.ps1 ] && cp -f start_flask.ps1 "$PACKAGE_DIR/" 2>/dev/null
[ -f start_flask.vbs ] && cp -f start_flask.vbs "$PACKAGE_DIR/" 2>/dev/null
[ -f start_flask_silent.vbs ] && cp -f start_flask_silent.vbs "$PACKAGE_DIR/" 2>/dev/null
[ -f create_shortcut.vbs ] && cp -f create_shortcut.vbs "$PACKAGE_DIR/" 2>/dev/null
[ -f build_launcher.bat ] && cp -f build_launcher.bat "$PACKAGE_DIR/" 2>/dev/null

# Copy Mac/Linux start scripts
echo "[6/8] Copying Mac/Linux scripts..."
[ -f run_flask.sh ] && cp -f run_flask.sh "$PACKAGE_DIR/" 2>/dev/null
[ -f start_server.sh ] && cp -f start_server.sh "$PACKAGE_DIR/" 2>/dev/null
[ -f cleanup_for_deployment.sh ] && cp -f cleanup_for_deployment.sh "$PACKAGE_DIR/" 2>/dev/null

# Copy documentation
echo "[7/8] Copying documentation..."
[ -f README.md ] && cp -f README.md "$PACKAGE_DIR/" 2>/dev/null
[ -f WINDOWS_SETUP.md ] && cp -f WINDOWS_SETUP.md "$PACKAGE_DIR/" 2>/dev/null
[ -f QUICK_START_ICON.md ] && cp -f QUICK_START_ICON.md "$PACKAGE_DIR/" 2>/dev/null
[ -f CREATE_ICON_SHORTCUT.md ] && cp -f CREATE_ICON_SHORTCUT.md "$PACKAGE_DIR/" 2>/dev/null
[ -f RENDER_DEPLOYMENT.md ] && cp -f RENDER_DEPLOYMENT.md "$PACKAGE_DIR/" 2>/dev/null
[ -f DEPLOYMENT_CHECKLIST.md ] && cp -f DEPLOYMENT_CHECKLIST.md "$PACKAGE_DIR/" 2>/dev/null
[ -f BUILD_EXE_LAUNCHER.md ] && cp -f BUILD_EXE_LAUNCHER.md "$PACKAGE_DIR/" 2>/dev/null

# Create empty directories that might be needed
echo "[8/8] Creating necessary directories..."
mkdir -p "$PACKAGE_DIR/resumes"
mkdir -p "$PACKAGE_DIR/generated_resumes"

# Create a README for the friend
echo "Creating README for recipient..."
cat > "$PACKAGE_DIR/README_FOR_FRIEND.md" << 'EOF'
# Email Notifications Flask Application

## Quick Start

### Windows:
1. Install Python 3.8+ from https://www.python.org/downloads/
2. Open Command Prompt in this folder
3. Run: `pip install -r requirements.txt`
4. Copy `env_example.txt` to `.env` and add your GROQ_API_KEY
5. Double-click `start_flask_simple.bat` to start

### Mac/Linux:
1. Install Python 3.8+
2. Run: `pip install -r requirements.txt`
3. Copy `env_example.txt` to `.env` and add your GROQ_API_KEY
4. Run: `python app.py`

## Configuration

1. Copy `env_example.txt` to `.env`
2. Add your GROQ_API_KEY in `.env` file
3. Update `email.json` with your email credentials if needed

## Documentation

- `WINDOWS_SETUP.md` - Detailed Windows setup guide
- `QUICK_START_ICON.md` - Create desktop shortcut
- `RENDER_DEPLOYMENT.md` - Deploy to Render cloud

## Support

If you encounter issues, check the documentation files or contact the sender.
EOF

echo ""
echo "========================================"
echo "Package created successfully!"
echo "========================================"
echo ""
echo "Package location: $PACKAGE_DIR"
echo ""
echo "Next steps:"
echo "1. Review the package folder"
echo "2. Create a ZIP file: zip -r ${PACKAGE_DIR}.zip $PACKAGE_DIR"
echo "3. Share the ZIP file with your friend"
echo ""
echo "IMPORTANT: Make sure email.json doesn't contain sensitive data"
echo "           or inform your friend to update it with their own credentials."
echo ""


