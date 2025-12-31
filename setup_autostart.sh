#!/bin/bash

# Setup script to install Flask server auto-startup on macOS

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_NAME="com.emailnotifications.flask.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_PATH="$LAUNCH_AGENTS_DIR/$PLIST_NAME"

echo "🚀 Setting up Flask server auto-startup..."
echo ""

# Check if LaunchAgents directory exists
if [ ! -d "$LAUNCH_AGENTS_DIR" ]; then
    echo "Creating LaunchAgents directory..."
    mkdir -p "$LAUNCH_AGENTS_DIR"
fi

# Copy plist file
echo "📋 Copying plist file to LaunchAgents..."
cp "$SCRIPT_DIR/$PLIST_NAME" "$PLIST_PATH"

# Make sure start_server.sh is executable
chmod +x "$SCRIPT_DIR/start_server.sh"

# Unload existing service if it exists
if launchctl list | grep -q "com.emailnotifications.flask"; then
    echo "🛑 Unloading existing service..."
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
fi

# Load the service
echo "✅ Loading launch agent..."
launchctl load "$PLIST_PATH"

# Start the service immediately
echo "▶️  Starting Flask server..."
launchctl start com.emailnotifications.flask

echo ""
echo "✅ Setup complete!"
echo ""
echo "The Flask server will now automatically start when you log in."
echo ""
echo "To check if it's running:"
echo "  curl http://localhost:5002/"
echo ""
echo "To view logs:"
echo "  tail -f $SCRIPT_DIR/flask_server.log"
echo ""
echo "To stop the service:"
echo "  launchctl stop com.emailnotifications.flask"
echo ""
echo "To remove auto-startup:"
echo "  launchctl unload $PLIST_PATH"

