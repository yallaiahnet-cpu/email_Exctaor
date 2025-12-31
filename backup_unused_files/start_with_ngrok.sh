#!/bin/bash

# Start Flask app in background
cd /Users/yonteru/Documents/Email_Notifications
source venv/bin/activate
python app.py &

# Wait a bit for Flask to start
sleep 2

# Start ngrok tunnel
echo "Starting ngrok tunnel..."
ngrok http 5002 > ngrok.log 2>&1 &

# Wait a bit for ngrok to start
sleep 3

# Get the public URL
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*"' | head -1 | cut -d'"' -f4)

if [ -n "$PUBLIC_URL" ]; then
    echo "✅ Public URL: $PUBLIC_URL"
    echo "Flask app is running on localhost:5002"
    echo "ngrok is forwarding to: $PUBLIC_URL"
else
    echo "❌ Could not get ngrok URL. Check ngrok.log"
fi

