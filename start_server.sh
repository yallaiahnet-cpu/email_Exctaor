#!/bin/bash

# Email Notifications Flask Server Startup Script
# This script starts the Flask application on port 5002

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Set Python path
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Ensure cloudflared is available
if ! command -v cloudflared >/dev/null 2>&1; then
    echo "Error: cloudflared is not installed or not in PATH."
    exit 1
fi

# Start Flask application
echo "Starting Email Notifications Flask Server on port 5002..."
echo "Script directory: $SCRIPT_DIR"
echo "Time: $(date)"

# Run the Flask app
# Use venv Python if available, otherwise system Python
if [ -f "$SCRIPT_DIR/venv/bin/python3" ]; then
    PYTHON3="$SCRIPT_DIR/venv/bin/python3"
    echo "Using venv Python: $PYTHON3"
elif [ -f "$SCRIPT_DIR/.venv/bin/python3" ]; then
    PYTHON3="$SCRIPT_DIR/.venv/bin/python3"
    echo "Using .venv Python: $PYTHON3"
else
    PYTHON3=$(which python3)
    if [ -z "$PYTHON3" ]; then
        PYTHON3="/usr/local/bin/python3"
    fi
    echo "Using system Python: $PYTHON3"
fi

echo "Launching Flask app with $PYTHON3 ..."
$PYTHON3 app.py &
APP_PID=$!
echo "Flask app started with PID $APP_PID"

cleanup() {
    echo "Stopping Flask app (PID $APP_PID)..."
    kill "$APP_PID" 2>/dev/null
    wait "$APP_PID" 2>/dev/null
}

trap cleanup EXIT

echo "Starting Cloudflare Tunnel to http://localhost:5002 ..."
cloudflared tunnel --url http://localhost:5002

wait "$APP_PID"
