#!/usr/bin/env python3
"""
Flask App Launcher for Windows
This script can be compiled to .exe with a custom icon using PyInstaller
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def find_python():
    """Find the best Python executable to use"""
    script_dir = Path(__file__).parent
    
    # Try venv first
    venv_python = script_dir / "venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    
    # Try .venv
    dotvenv_python = script_dir / ".venv" / "Scripts" / "python.exe"
    if dotvenv_python.exists():
        return str(dotvenv_python)
    
    # Use system Python
    return sys.executable

def start_flask():
    """Start the Flask application"""
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    python_cmd = find_python()
    app_file = script_dir / "app.py"
    
    if not app_file.exists():
        print(f"❌ Error: app.py not found in {script_dir}")
        input("Press Enter to exit...")
        return
    
    print("=" * 50)
    print("🚀 Starting Email Notifications Flask Server")
    print("=" * 50)
    print(f"📁 Directory: {script_dir}")
    print(f"🐍 Python: {python_cmd}")
    print(f"🌐 Server: http://localhost:5002")
    print("=" * 50)
    print("\n💡 Tip: Keep this window open while the server is running")
    print("   Press Ctrl+C to stop the server\n")
    print("-" * 50)
    print()
    
    try:
        # Start Flask app
        subprocess.run([python_cmd, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting Flask app: {e}")
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    start_flask()


