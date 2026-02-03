# 🚀 Running the Application Locally

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Virtual environment** (recommended)

## Step-by-Step Setup

### 1. Navigate to Project Directory
```bash
cd /Users/yonteru/Documents/Email_Notifications
```

### 2. Create and Activate Virtual Environment

**On macOS/Linux:**
```bash
# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

The app primarily uses `email.json` for email credentials, but you may want to set up a `.env` file for the Groq API key:

```bash
# Copy the example file
cp env_example.txt .env

# Edit .env and add your GROQ_API_KEY (if needed)
# The app will work with email.json alone, but Groq API key is needed for resume generation
```

**Note:** The app loads email credentials from `email.json` automatically, so you don't need to set SMTP credentials in `.env` unless you want to override.

### 5. Verify Required Files

Make sure these files exist:
- ✅ `email.json` - Contains email account credentials
- ✅ `bold_words.json` - Contains keywords for resume bolding (optional)
- ✅ `templates/` - HTML templates directory
- ✅ `app.py` - Main application file

### 6. Run the Application

**Option 1: Direct Python execution**
```bash
python app.py
```

**Option 2: Using Flask command**
```bash
flask run --host=0.0.0.0 --port=5002
```

**Option 3: Using Python module**
```bash
python -m flask run --host=0.0.0.0 --port=5002
```

### 7. Access the Application

Once running, open your browser and navigate to:
- **Main Interface:** http://localhost:5002
- **API Endpoints:** http://localhost:5002/api/...

The app runs on **port 5002** by default.

## Troubleshooting

### Port Already in Use
If port 5002 is already in use, you can change it:
```python
# Edit app.py, line 1478
app.run(debug=True, host='0.0.0.0', port=5003)  # Change port number
```

Or run with a different port:
```bash
flask run --host=0.0.0.0 --port=5003
```

### Missing Dependencies
If you get import errors, make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Email Configuration Issues
- Verify `email.json` exists and has valid email credentials
- Check that app passwords are correctly formatted (spaces between groups)
- Ensure the email account has "Less secure app access" enabled or uses App Passwords

### Groq API Key
If you need resume generation features, make sure `GROQ_API_KEY` is set in your `.env` file or environment variables.

## Quick Start (One Command)

If everything is already set up:
```bash
source venv/bin/activate && python app.py
```

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the Flask server.

