# Auto-Start Flask Server on macOS

This guide will help you set up the Flask server to automatically start when your laptop powers on.

## Method 1: Using LaunchAgent (Recommended)

1. **Copy the plist file to LaunchAgents directory:**
   ```bash
   cp com.emailnotifications.flask.plist ~/Library/LaunchAgents/
   ```

2. **Load the launch agent:**
   ```bash
   launchctl load ~/Library/LaunchAgents/com.emailnotifications.flask.plist
   ```

3. **To start it immediately (without restarting):**
   ```bash
   launchctl start com.emailnotifications.flask
   ```

4. **To stop the service:**
   ```bash
   launchctl stop com.emailnotifications.flask
   ```

5. **To unload (remove from startup):**
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.emailnotifications.flask.plist
   ```

## Method 2: Using Login Items (Simpler)

1. Open **System Settings** (or System Preferences on older macOS)
2. Go to **General** → **Login Items**
3. Click the **+** button
4. Navigate to `/Users/yonteru/Documents/Email_Notifications/start_server.sh`
5. Select it and click **Add**

## Verify it's running

After startup, check if the server is running:
```bash
curl http://localhost:5002/
```

Or check the logs:
```bash
tail -f /Users/yonteru/Documents/Email_Notifications/flask_server.log
```

## Troubleshooting

- If the server doesn't start, check the error log:
  ```bash
  cat /Users/yonteru/Documents/Email_Notifications/flask_server_error.log
  ```

- Make sure Python 3 is installed and accessible:
  ```bash
  which python3
  ```

- Make sure all dependencies are installed:
  ```bash
  pip3 install flask python-dotenv langchain-groq
  ```

