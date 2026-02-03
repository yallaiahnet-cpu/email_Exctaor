# 🎯 Build .exe Launcher with Custom Icon

This guide shows you how to create a standalone `.exe` file with a custom icon that you can double-click to start your Flask app.

## 📦 Step 1: Install PyInstaller

Open Command Prompt or PowerShell and run:

```cmd
pip install pyinstaller
```

## 🎨 Step 2: Get or Create an Icon

### Option A: Download a Free Icon
1. Visit [Flaticon](https://www.flaticon.com) or [Icons8](https://icons8.com)
2. Search for "flask", "server", "web", or "python"
3. Download as `.ico` format
4. Save it as `flask_icon.ico` in your project folder

### Option B: Use Python Icon
If Python is installed, you can extract its icon:
- Location: `C:\Program Files\Python3x\python.exe`
- Use an icon extractor tool or download from online

### Option C: Convert Image to Icon
1. Use [convertio.co](https://convertio.co/png-ico/) or [icoconvert.com](https://icoconvert.com)
2. Upload your image (PNG, JPG, etc.)
3. Download as `.ico` format
4. Save as `flask_icon.ico`

## 🔨 Step 3: Build the .exe

Open Command Prompt in your project directory and run:

### Basic Build (No Icon):
```cmd
pyinstaller --onefile --windowed --name "Flask App Launcher" launcher.py
```

### Build with Custom Icon:
```cmd
pyinstaller --onefile --windowed --icon=flask_icon.ico --name "Flask App Launcher" launcher.py
```

### Advanced Build (Recommended):
```cmd
pyinstaller --onefile ^
    --windowed ^
    --icon=flask_icon.ico ^
    --name "Flask App Launcher" ^
    --add-data "templates;templates" ^
    --add-data "email.json;." ^
    --add-data "otter_links.json;." ^
    --hidden-import=flask ^
    --hidden-import=werkzeug ^
    launcher.py
```

**Note:** The `^` is for line continuation in Windows CMD. In PowerShell, use `` ` `` instead.

## 📁 Step 4: Find Your .exe

After building, your `.exe` file will be in:
```
dist\Flask App Launcher.exe
```

## 🚀 Step 5: Use Your Launcher

1. **Copy `Flask App Launcher.exe`** to your desktop or any location
2. **Double-click** to start the Flask app
3. The app will open in a console window showing server status

## 🎯 Quick Build Script

Create a file `build_launcher.bat`:

```batch
@echo off
echo Building Flask App Launcher...
pyinstaller --onefile --windowed --icon=flask_icon.ico --name "Flask App Launcher" launcher.py
echo.
echo Build complete! Check dist\Flask App Launcher.exe
pause
```

Then double-click `build_launcher.bat` to build.

## 🔧 Troubleshooting

### Issue: "pyinstaller is not recognized"
**Solution:** Install PyInstaller:
```cmd
pip install pyinstaller
```

### Issue: Icon not showing
**Solution:** 
- Make sure icon file is `.ico` format (not PNG/JPG)
- Use full path: `--icon=C:\full\path\to\flask_icon.ico`
- Try a different icon file

### Issue: .exe doesn't find app.py
**Solution:** The launcher looks for `app.py` in the same directory as the `.exe`. Make sure:
- `app.py` is in the same folder as the `.exe`, OR
- Use the advanced build command with `--add-data` to bundle files

### Issue: Missing dependencies
**Solution:** Add hidden imports:
```cmd
pyinstaller --onefile --windowed --hidden-import=flask --hidden-import=werkzeug --hidden-import=dotenv launcher.py
```

## 💡 Tips

1. **Test First:** Run `python launcher.py` to make sure it works before building
2. **Icon Size:** Use 256x256 or 512x512 icon for best quality
3. **File Size:** The `.exe` will be large (20-50MB) - this is normal
4. **Antivirus:** Some antivirus may flag PyInstaller .exe files - this is a false positive
5. **Distribution:** You can share the `.exe` with others, but they'll need Python installed (unless you bundle everything)

## 🎨 Alternative: Simple VBScript Method

If you don't want to build an .exe, use the VBScript method:

1. **Double-click `create_shortcut.vbs`** to create desktop shortcut
2. **Right-click shortcut** → Properties → Change Icon
3. **Select your icon** and click OK

This is simpler and doesn't require PyInstaller!


