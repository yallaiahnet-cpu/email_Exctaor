# 🚀 Render Deployment Checklist

## Quick Reference: What to Clean

### ❌ Remove/Backup (Not needed for web app):
- `backup/` - Old backup files
- `backup_unused_files/` - Unused files
- `chrome_notes_extension/` - Chrome extension (not needed for web)
- `job_autofill_extension/` - Chrome extension (not needed for web)
- `jd_extractor_extension/` - Chrome extension (not needed for web)
- `app2.py` - Duplicate/unused file
- `*.log` - Log files
- `*.sh` - Local setup scripts (setup_autostart.sh, start_server.sh, run_flask.sh)
- `com.emailnotifications.flask.plist` - macOS specific
- `*.png`, `*.svg` in root - Image files (unless used in templates)
- `*.html` in root - HTML files (unless needed)
- `*.zip` - Archive files
- `__pycache__/` - Python cache (auto-ignored)

### ✅ Keep (Required for app):
- `app.py` - Main Flask app
- `requirements.txt` - Dependencies
- `Procfile` - Render deployment config
- `render.yaml` - Optional Render config
- `templates/` - All HTML templates
- `email.json` - Email credentials (⚠️ sensitive!)
- `otter_links.json` - Data file
- `sent_emails.json` - Data file
- `cleaning_jd.py` - Email extraction module
- `send_email.py` - Email sending module
- `llm_exctration.py` - LLM extraction module
- `document_creation.py` - Resume generation module
- `job_scraper.py` - Job scraping module
- `resumes/` - Resume data (optional)
- `generated_resumes/` - Generated resumes (optional)
- Other `.json` data files as needed

## 🔧 Quick Cleanup

**On Mac/Linux:**
```bash
./cleanup_for_deployment.sh
```

**On Windows:**
```cmd
mkdir deployment_backup
move backup deployment_backup\
move backup_unused_files deployment_backup\
move chrome_notes_extension deployment_backup\
move job_autofill_extension deployment_backup\
move jd_extractor_extension deployment_backup\
move app2.py deployment_backup\
move *.log deployment_backup\
move *.sh deployment_backup\
```

Or manually move files to `deployment_backup/` folder.

## 🔐 Environment Variables (Set in Render Dashboard)

**Required:**
- `GROQ_API_KEY` - Your Groq API key

**Optional:**
- `FLASK_ENV=production`
- `PORT=10000` (auto-set by Render)

## 📝 Deployment Steps

1. ✅ Clean up project (run cleanup script)
2. ✅ Commit all files (including email.json - contains sensitive data)
3. ✅ Push to Git repository
4. ✅ Create new Web Service in Render
5. ✅ Connect repository
6. ✅ Set environment variables
7. ✅ Deploy!

## ⚠️ Security Note

`email.json` contains SMTP passwords. Options:
1. **Keep it** (current setup) - Simple but less secure
2. **Move to env vars** (recommended) - More secure, requires code changes

See `RENDER_DEPLOYMENT.md` for detailed instructions.

