# Render Deployment Fix

## Issue
Render was trying to use Docker instead of Python buildpack.

## Solution

### Option 1: Use render.yaml (Recommended)
The `render.yaml` file is already configured correctly. Make sure in Render dashboard:

1. Go to your service settings
2. Under "Build & Deploy":
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment**: `Python 3`
   - **Docker**: Make sure Docker is **DISABLED**

### Option 2: Manual Configuration in Render Dashboard

1. **Service Type**: Web Service
2. **Environment**: Python 3
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. **Auto-Deploy**: Yes (if you want)

### Required Environment Variables

Set these in Render Dashboard → Environment:

- `GROQ_API_KEY` - Your Groq API key (if using resume generation)
- `FLASK_ENV=production`
- `PORT` - Automatically set by Render

### Important Files

- ✅ `Procfile` - Tells Render how to start the app
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration (optional but recommended)

### If Still Getting Docker Error

1. In Render Dashboard, go to your service
2. Settings → Build & Deploy
3. Make sure "Docker" is **NOT** selected
4. Select "Python" as the environment
5. Redeploy

