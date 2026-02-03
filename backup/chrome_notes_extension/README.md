# Personal Notes Keeper - Chrome Extension

A simple, secure, and beautiful Chrome extension to keep your personal notes and data. All data is stored locally in your browser using Chrome's storage API.

## Features

- ✅ **Create Notes**: Add notes with title, content, and tags
- ✅ **View Notes**: Browse all your notes in a clean, organized list
- ✅ **Edit Notes**: Update existing notes easily
- ✅ **Delete Notes**: Remove notes you no longer need
- ✅ **Search**: Quickly find notes by title, content, or tags
- ✅ **Tags**: Organize notes with custom tags
- ✅ **Local Storage**: All data is stored locally in your browser (privacy-first)
- ✅ **Beautiful UI**: Modern, gradient-based design with smooth animations

## Installation

### Step 1: Download the Extension

1. Make sure all files are in the `chrome_notes_extension` folder:
   - `manifest.json`
   - `popup.html`
   - `popup.js`
   - `styles.css`
   - `icons/` folder (see Step 2)

### Step 2: Create Icons (Optional but Recommended)

Create an `icons` folder inside `chrome_notes_extension` and add three icon files:
- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels)
- `icon128.png` (128x128 pixels)

You can use any image editor or online tool to create these icons. If you don't have icons, the extension will still work but may show a default icon.

### Step 3: Load the Extension in Chrome

1. Open Google Chrome
2. Go to `chrome://extensions/` (or navigate via Menu → Extensions → Manage Extensions)
3. Enable **Developer mode** (toggle in the top-right corner)
4. Click **Load unpacked**
5. Select the `chrome_notes_extension` folder
6. The extension should now appear in your extensions list

### Step 4: Pin the Extension (Optional)

1. Click the puzzle piece icon (🧩) in Chrome's toolbar
2. Find "Personal Notes Keeper" in the list
3. Click the pin icon to keep it visible in your toolbar

## Usage

1. **Click the extension icon** in your Chrome toolbar
2. **Add a Note**:
   - Click the "Add Note" tab
   - Enter a title and content
   - Optionally add tags (comma-separated)
   - Click "Save Note"

3. **View Notes**:
   - Click the "My Notes" tab
   - All notes are displayed with newest first
   - Click on a note to expand and see full content

4. **Edit a Note**:
   - Click on a note to expand it
   - Click the "Edit" button
   - Make your changes
   - Click "Update Note"

5. **Delete a Note**:
   - Click on a note to expand it
   - Click the "Delete" button
   - Confirm deletion

6. **Search Notes**:
   - Use the search box in the "My Notes" tab
   - Search by title, content, or tags

## Data Storage

- All notes are stored locally in your browser using Chrome's `chrome.storage.local` API
- Data is **NOT** synced to any external server
- Data persists even after closing the browser
- To clear all data: Go to `chrome://extensions/` → Find the extension → Click "Remove" (this will delete all notes)

## Privacy

- ✅ All data is stored locally on your device
- ✅ No data is sent to external servers
- ✅ No tracking or analytics
- ✅ Completely private and secure

## Troubleshooting

**Extension not loading?**
- Make sure Developer mode is enabled
- Check that all files are in the correct folder structure
- Check the browser console for errors (F12)

**Notes not saving?**
- Make sure the extension has storage permissions (should be automatic)
- Check browser console for errors

**Icons not showing?**
- Create the `icons` folder and add the icon files
- Or the extension will use default Chrome icons

## File Structure

```
chrome_notes_extension/
├── manifest.json          # Extension configuration
├── popup.html             # Main UI
├── popup.js               # JavaScript functionality
├── styles.css             # Styling
├── icons/                 # Extension icons (create this folder)
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── README.md             # This file
```

## Future Enhancements (Possible Features)

- Export notes to JSON/CSV
- Import notes from file
- Rich text editing
- Note categories/folders
- Dark mode
- Note encryption
- Sync across devices (optional)

## License

Free to use and modify for personal use.

---

**Enjoy keeping your notes organized! 📝**

