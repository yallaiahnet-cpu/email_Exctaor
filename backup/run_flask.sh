#!/bin/bash

# Wrapper script to run Flask app with proper environment
cd /Users/yonteru/Documents/Email_Notifications

# Activate venv and run
if [ -f "venv/bin/python3" ]; then
    exec venv/bin/python3 app.py
elif [ -f ".venv/bin/python3" ]; then
    exec .venv/bin/python3 app.py
else
    exec python3 app.py
fi

