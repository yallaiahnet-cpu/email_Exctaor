#!/bin/bash

# Script to clean up project folder for Render deployment
# This script moves unnecessary files to a backup directory

echo "🧹 Starting cleanup for Render deployment..."

# Create backup directory
BACKUP_DIR="deployment_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup directory: $BACKUP_DIR"

# Move unnecessary directories
if [ -d "backup" ]; then
    echo "  → Moving backup/ to $BACKUP_DIR/"
    mv backup "$BACKUP_DIR/"
fi

if [ -d "backup_unused_files" ]; then
    echo "  → Moving backup_unused_files/ to $BACKUP_DIR/"
    mv backup_unused_files "$BACKUP_DIR/"
fi

if [ -d "chrome_notes_extension" ]; then
    echo "  → Moving chrome_notes_extension/ to $BACKUP_DIR/"
    mv chrome_notes_extension "$BACKUP_DIR/"
fi

if [ -d "job_autofill_extension" ]; then
    echo "  → Moving job_autofill_extension/ to $BACKUP_DIR/"
    mv job_autofill_extension "$BACKUP_DIR/"
fi

if [ -d "jd_extractor_extension" ]; then
    echo "  → Moving jd_extractor_extension/ to $BACKUP_DIR/"
    mv jd_extractor_extension "$BACKUP_DIR/"
fi

# Move unnecessary files
if [ -f "app2.py" ]; then
    echo "  → Moving app2.py to $BACKUP_DIR/"
    mv app2.py "$BACKUP_DIR/"
fi

if [ -f "com.emailnotifications.flask.plist" ]; then
    echo "  → Moving com.emailnotifications.flask.plist to $BACKUP_DIR/"
    mv com.emailnotifications.flask.plist "$BACKUP_DIR/"
fi

# Move shell scripts (optional - you might want to keep some)
if [ -f "setup_autostart.sh" ]; then
    echo "  → Moving setup_autostart.sh to $BACKUP_DIR/"
    mv setup_autostart.sh "$BACKUP_DIR/"
fi

if [ -f "start_server.sh" ]; then
    echo "  → Moving start_server.sh to $BACKUP_DIR/"
    mv start_server.sh "$BACKUP_DIR/"
fi

if [ -f "run_flask.sh" ]; then
    echo "  → Moving run_flask.sh to $BACKUP_DIR/"
    mv run_flask.sh "$BACKUP_DIR/"
fi

# Move log files
echo "  → Moving log files to $BACKUP_DIR/"
mv *.log "$BACKUP_DIR/" 2>/dev/null || true

# Move image files (optional - keep if used in templates)
if [ -f "image.png" ]; then
    echo "  → Moving image.png to $BACKUP_DIR/"
    mv image.png "$BACKUP_DIR/"
fi

if [ -f "image copy.png" ]; then
    echo "  → Moving image copy.png to $BACKUP_DIR/"
    mv "image copy.png" "$BACKUP_DIR/"
fi

if [ -f "rainbow.png" ]; then
    echo "  → Moving rainbow.png to $BACKUP_DIR/"
    mv rainbow.png "$BACKUP_DIR/"
fi

if [ -f "business_card.svg" ]; then
    echo "  → Moving business_card.svg to $BACKUP_DIR/"
    mv business_card.svg "$BACKUP_DIR/"
fi

# Move HTML files in root (if not needed)
if [ -f "Spartexai.html" ]; then
    echo "  → Moving Spartexai.html to $BACKUP_DIR/"
    mv Spartexai.html "$BACKUP_DIR/"
fi

if [ -f "US_Aura_Staffing.html" ]; then
    echo "  → Moving US_Aura_Staffing.html to $BACKUP_DIR/"
    mv US_Aura_Staffing.html "$BACKUP_DIR/"
fi

# Move zip files
if [ -f "chrome_notes_extension.zip" ]; then
    echo "  → Moving chrome_notes_extension.zip to $BACKUP_DIR/"
    mv chrome_notes_extension.zip "$BACKUP_DIR/"
fi

echo ""
echo "✅ Cleanup complete!"
echo "📁 Backup created at: $BACKUP_DIR"
echo ""
echo "⚠️  IMPORTANT: Review the backup directory before deleting it."
echo "💡 You can restore files with: mv $BACKUP_DIR/* ."
echo ""
echo "📋 Next steps:"
echo "   1. Review RENDER_DEPLOYMENT.md for deployment instructions"
echo "   2. Ensure email.json is committed (contains sensitive data)"
echo "   3. Set environment variables in Render dashboard"
echo "   4. Push to Git and deploy!"


