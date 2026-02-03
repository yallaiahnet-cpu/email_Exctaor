# Render Deployment Guide

This guide will help you deploy your Flask application to Render.

## 📋 Pre-Deployment Checklist

### 1. Files to Clean/Remove (Optional but Recommended)

These files/folders can be removed or moved to a separate backup before deployment:

```
❌ Remove/Backup:
- __pycache__/ (already in .gitignore)
- venv/ (already in .gitignore)
- backup/ (unused backup files)
- backup_unused_files/ (unused files)
- chrome_notes_extension/ (Chrome extension, not needed for web app)
- job_autofill_extension/ (Chrome extension, not needed for web app)
- jd_extractor_extension/ (Chrome extension, not needed for web app)
- *.log files (already in .gitignore)
- app2.py (duplicate/unused)
- com.emailnotifications.flask.plist (macOS specific)
- setup_autostart.sh (local setup script)
- start_server.sh (local setup script)
- run_flask.sh (local setup script)
- *.svg, *.png (unless needed for templates)
- *.html files in root (unless needed)
```

### 2. Required Files to Keep

```
✅ Keep:
- app.py (main Flask application)
- requirements.txt (dependencies)
- Procfile (for Render)
- render.yaml (optional, for Render config)
- templates/ (all HTML templates)
- email.json (contains email credentials - KEEP PRIVATE!)
- otter_links.json (data file)
- sent_emails.json (data file)
- resumes/ (if you want to keep resume data)
- generated_resumes/ (if you want to keep generated resumes)
- cleaning_jd.py
- send_email.py
- llm_exctration.py
- document_creation.py
- job_scraper.py
- bold_words.json (if used)
- nvoids_jobs.json (if used)
- resunedotnet.json (if used)
- senior_aws_data_engineer_resume.json (if used)
```

## 🔐 Environment Variables Setup in Render

In your Render dashboard, add these environment variables:

### Required:
```
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=production
PORT=10000
```

### Optional (if you need them):
```
FLASK_DEBUG=False
```

**Note:** `email.json` contains sensitive SMTP credentials. You have two options:
1. **Keep email.json in your repo** (not recommended for security)
2. **Move credentials to environment variables** (recommended)

## 📝 Steps to Deploy

### Step 1: Clean Up Project (Optional)

Create a script to clean up unnecessary files:

```bash
# Create a backup directory
mkdir -p deployment_backup

# Move unnecessary files
mv backup deployment_backup/
mv backup_unused_files deployment_backup/
mv chrome_notes_extension deployment_backup/
mv job_autofill_extension deployment_backup/
mv jd_extractor_extension deployment_backup/
mv app2.py deployment_backup/
mv *.log deployment_backup/ 2>/dev/null || true
mv *.sh deployment_backup/ 2>/dev/null || true
mv com.emailnotifications.flask.plist deployment_backup/ 2>/dev/null || true
```

### Step 2: Update .gitignore

Ensure your `.gitignore` includes:
```
.env
*.log
__pycache__/
venv/
*.pyc
*.pyo
*.pyd
.Python
```

### Step 3: Update app.py for Production

The app already uses `host='0.0.0.0'` which is good. Render will use the PORT environment variable automatically.

### Step 4: Deploy to Render

1. **Push to GitHub/GitLab/Bitbucket**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create New Web Service in Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your repository
   - Select your repository and branch

3. **Configure Service**
   - **Name:** email-notifications-api (or your preferred name)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan:** Free tier or paid (Free tier has limitations)

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add `GROQ_API_KEY` with your API key
   - Add `FLASK_ENV=production`
   - Add `PORT=10000` (Render sets this automatically, but good to have)

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app
   - Your app will be available at: `https://your-service-name.onrender.com`

## 🔒 Security Recommendations

### Option 1: Keep email.json (Current Setup)
- ✅ Simple, no code changes needed
- ❌ Sensitive data in repository
- ⚠️ Make sure email.json is NOT in .gitignore (it's needed for the app)

### Option 2: Move to Environment Variables (Recommended)
Update `app.py` to read from environment variables instead of `email.json`:

```python
# Instead of loading from email.json, use environment variables
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
```

Then add to Render environment variables:
```
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

## 📊 Render Configuration

### Free Tier Limitations:
- Services spin down after 15 minutes of inactivity
- Cold starts can take 30-60 seconds
- Limited build minutes per month

### Paid Tier Benefits:
- Always-on services
- Faster cold starts
- More build minutes

## 🐛 Troubleshooting

### Issue: Build fails
- Check that `requirements.txt` has all dependencies
- Ensure Python version is compatible (Render uses Python 3.11 by default)

### Issue: App crashes on startup
- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure `email.json` exists and is valid JSON

### Issue: Port binding error
- Render automatically sets PORT environment variable
- Gunicorn should use `$PORT` (already configured in Procfile)

### Issue: Cannot find email.json
- Ensure `email.json` is committed to your repository
- Check file path in `app.py` (should use `os.getcwd()`)

## 📁 Final Project Structure (Recommended)

```
Email_Notifications/
├── app.py
├── requirements.txt
├── Procfile
├── render.yaml (optional)
├── .gitignore
├── email.json (⚠️ contains sensitive data)
├── templates/
│   └── [all HTML files]
├── cleaning_jd.py
├── send_email.py
├── llm_exctration.py
├── document_creation.py
├── job_scraper.py
├── otter_links.json
├── sent_emails.json
├── resumes/ (optional)
├── generated_resumes/ (optional)
└── [other JSON data files as needed]
```

## ✅ Post-Deployment

1. Test all endpoints
2. Verify email sending works
3. Check that templates load correctly
4. Monitor logs for any errors
5. Set up custom domain (optional, paid feature)

## 🔄 Updating the Deployment

After making changes:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will automatically rebuild and redeploy.


