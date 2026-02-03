# Windows Setup Guide

This guide helps you set up and run the Email Notifications Flask application on Windows.

## 📋 Prerequisites

1. **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   - Verify installation: Open Command Prompt and run `python --version`

2. **Git** (optional) - For cloning the repository
   - Download from [git-scm.com](https://git-scm.com/download/win)

## 🚀 Quick Start

### Option 1: Simple Batch Script (Recommended for beginners)

1. Double-click `start_flask_simple.bat`
2. The Flask app will start automatically
3. Open your browser to `http://localhost:5002`

### Option 2: Full-Featured Batch Script

1. Double-click `start_flask.bat`
2. More detailed output and error handling
3. Server available at `http://localhost:5002`

### Option 3: PowerShell Script (Modern Windows)

1. Right-click `start_flask.ps1` → "Run with PowerShell"
2. If you get an execution policy error, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Then run: `.\start_flask.ps1`

## 🔧 Manual Setup

### Step 1: Install Dependencies

Open Command Prompt or PowerShell in the project directory:

```cmd
pip install -r requirements.txt
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. Copy `env_example.txt` to `.env`
2. Edit `.env` with your credentials:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Step 4: Run the Application

**Using Command Prompt:**
```cmd
python app.py
```

**Using PowerShell:**
```powershell
python app.py
```

**Using the batch script:**
```cmd
start_flask.bat
```

## 📝 Available Start Scripts

| Script | Description | Best For |
|--------|-------------|----------|
| `start_flask_simple.bat` | Quick start, minimal output | Beginners, quick testing |
| `start_flask.bat` | Full-featured with error handling | Daily use, debugging |
| `start_flask.ps1` | PowerShell version with colored output | Modern Windows, better UX |

## 🐛 Troubleshooting

### Issue: "Python is not recognized"

**Solution:**
- Reinstall Python and check "Add Python to PATH"
- Or add Python manually to PATH:
  1. Find Python installation (usually `C:\Python3x\` or `C:\Users\YourName\AppData\Local\Programs\Python\Python3x\`)
  2. Add to PATH: Settings → System → Advanced → Environment Variables → Path → Edit → Add Python path

### Issue: "Module not found" errors

**Solution:**
```cmd
pip install -r requirements.txt
```

If using virtual environment:
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Port 5002 already in use

**Solution:**
1. Find process using port 5002:
   ```cmd
   netstat -ano | findstr :5002
   ```
2. Kill the process (replace PID with actual process ID):
   ```cmd
   taskkill /PID <PID> /F
   ```
3. Or change port in `app.py` (last line):
   ```python
   app.run(debug=True, host='0.0.0.0', port=5003)  # Change 5002 to 5003
   ```

### Issue: PowerShell execution policy error

**Solution:**
Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Virtual environment activation fails

**Solution:**
- Make sure you're in the project directory
- Try: `venv\Scripts\activate.bat` (not just `activate`)
- Or recreate virtual environment:
  ```cmd
  rmdir /s venv
  python -m venv venv
  venv\Scripts\activate
  ```

## 🔒 Security Notes

- Never commit `.env` file to Git (already in `.gitignore`)
- `email.json` contains SMTP passwords - keep it secure
- Use environment variables for production deployments

## 📚 Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Python Virtual Environments: https://docs.python.org/3/tutorial/venv.html
- Windows Command Prompt Guide: https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/

## 💡 Tips

1. **Use Virtual Environment**: Always use a virtual environment to avoid dependency conflicts
2. **Check Logs**: If something fails, check the terminal output for error messages
3. **Keep Updated**: Regularly update dependencies: `pip install --upgrade -r requirements.txt`
4. **Backup email.json**: Before making changes, backup your `email.json` file

## 🎯 Next Steps

After getting the app running:
1. Test the web interface at `http://localhost:5002`
2. Try the Email Extractor tool
3. Test other features (Job Scraper, Resume Generator, etc.)
4. See `RENDER_DEPLOYMENT.md` if you want to deploy to Render


