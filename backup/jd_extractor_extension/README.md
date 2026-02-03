# JD Extractor & LinkedIn Connector Chrome Extension

A Chrome extension that extracts job details from job descriptions and generates LinkedIn connection notes using AI.

## Features

- 🎯 Extract job details (Recruiter, Company, Location, Skills) from job descriptions
- 🤖 AI-powered extraction using Groq API
- 📦 **Batch Processing**: Paste multiple JDs at once - they'll be processed sequentially and auto-saved
- 💾 Save extracted JDs locally with date/time stamps
- ✏️ Edit saved job descriptions
- 📋 Copy LinkedIn connection notes to clipboard
- 📚 Scroll through all saved job descriptions
- 🎨 Deep blue theme interface
- 🔵 Round icon with "JD" label

## Installation

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `jd_extractor_extension` folder
5. The extension icon will appear in your toolbar

### Troubleshooting: Side Panel Not Opening

If clicking the icon doesn't open the side panel:

1. **Check Chrome version**: Side panels require Chrome 114 or later
   - Go to `chrome://version/` to check your version
   - Update Chrome if needed

2. **Manual open**:
   - Right-click the extension icon
   - Select "Open side panel" from the context menu

3. **Reload extension**:
   - Go to `chrome://extensions/`
   - Find "JD Extractor & LinkedIn Connector"
   - Click the reload button (🔄)

4. **Check console errors**:
   - Press F12 to open Developer Tools
   - Go to the "Console" tab
   - Click the extension icon
   - Look for any error messages (they'll help identify the issue)

5. **Verify permissions**:
   - Make sure "sidePanel" permission is granted
   - Check in `chrome://extensions/` → Your extension → "Details" → "Permissions"

## Setup

1. Make sure your Flask server is running on `http://localhost:5002`
2. Ensure you have `GROQ_API_KEY` in your `.env` file (optional - will use fallback if not available)
3. The extension will connect to your Flask server for AI-powered extraction

## Usage

1. Click the extension icon to open the sidebar
2. Paste a job description in the text area
3. Click "Extract & Generate Note" to extract details
4. Review and edit the extracted information
5. Click "Save" to store the JD locally
6. Click "View Saved JDs" to see all saved job descriptions
7. Edit, copy, or delete saved JDs as needed

## Files Structure

```
jd_extractor_extension/
├── manifest.json       # Extension manifest
├── background.js       # Service worker
├── sidebar.html        # Sidebar UI
├── sidebar.css         # Deep blue theme styles
├── sidebar.js          # Main functionality
├── content.js          # Content script
├── content.css         # Content styles
├── icons/              # Extension icons
└── README.md           # This file
```

## API Endpoint

The extension requires a Flask endpoint at `http://localhost:5002/extract_jd` that accepts:
- Method: POST
- Body: `{ "job_description": "..." }`
- Returns: `{ "recruiter_name": "...", "company_name": "...", "location": "...", "key_focus": "...", "linkedin_note": "..." }`

## Requirements

- Chrome browser
- Flask server running on localhost:5002
- GROQ_API_KEY in .env (optional - for AI extraction)

## Notes

- All data is stored locally in Chrome's storage
- The extension works offline for saved JDs
- AI extraction requires Flask server connection
- Fallback regex extraction works if AI is unavailable

