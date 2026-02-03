# Job Application Auto-Fill Chrome Extension

A robust Chrome extension that automatically fills job application forms with your resume data. Save time by auto-filling personal information, work experience, education, skills, and even uploading your resume file.

## Features

✨ **Smart Form Detection**
- Automatically detects form fields across major job sites
- Works with LinkedIn, Indeed, Greenhouse, Workday, and custom ATS systems
- Intelligent field matching by name, ID, placeholder, and label

📝 **Comprehensive Data Management**
- Personal information (name, email, phone, address, LinkedIn, GitHub)
- Multiple work experience entries with dates and descriptions
- Education history with degrees and GPA
- Skills and certifications
- Cover letter templates

📎 **Resume Auto-Upload**
- Upload and store your resume file (PDF/DOCX)
- Automatically attaches resume to file upload fields
- Supports multiple file formats

🎯 **Quick Actions**
- One-click form filling from extension popup
- Floating button on job application pages
- Export/Import your data as JSON

## Installation

1. **Download or Clone the Extension**
   ```bash
   cd job_autofill_extension
   ```

2. **Generate Icons** (if needed)
   ```bash
   pip install Pillow
   python generate_icons.py
   ```

3. **Load Extension in Chrome**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `job_autofill_extension` folder

## Usage

### Setting Up Your Data

1. **Click the extension icon** in your Chrome toolbar
2. **Fill in your information** across the tabs:
   - **Personal**: Name, email, phone, address, social links
   - **Experience**: Add each job with title, company, dates, and description
   - **Education**: Add degrees, schools, graduation years
   - **Skills**: Technical skills, certifications, languages
   - **Resume**: Upload resume file and cover letter template

3. **Save your data** - All information is stored locally in your browser

### Auto-Filling Forms

**Method 1: From Extension Popup**
- Click the extension icon
- Click "🔍 Fill Current Page" button
- The extension will automatically detect and fill form fields

**Method 2: Floating Button**
- Navigate to any job application page
- A floating "🚀 Fill Form" button appears in the bottom-right corner
- Click it to auto-fill the form

**Method 3: Manual Trigger**
- The extension automatically detects job application forms
- Look for the floating button on supported sites

## Supported Job Sites

- ✅ LinkedIn Easy Apply
- ✅ Indeed
- ✅ Greenhouse
- ✅ Lever
- ✅ Workday
- ✅ Custom ATS systems
- ✅ Company career pages

## Data Export/Import

### Export Your Data
1. Open extension popup
2. Click "📥 Export Data"
3. A JSON file will be downloaded with all your information

### Import Your Data
1. Open extension popup
2. Click "📤 Import Data"
3. Select your previously exported JSON file
4. All data will be restored

## Privacy & Security

🔒 **Your Data is Private**
- All data is stored locally in your browser
- No data is sent to external servers
- No tracking or analytics
- You have full control over your information

## Technical Details

### Field Detection
The extension uses multiple strategies to find form fields:
- Field name matching (firstName, email, etc.)
- Field ID matching
- Placeholder text matching
- Label text matching
- Common ATS field patterns

### Supported Field Types
- Text inputs
- Email inputs
- Phone inputs
- Textareas
- Select dropdowns
- Date pickers
- File uploads

## Troubleshooting

### Form Not Filling?
1. **Check if fields are detected**: Open browser console (F12) and look for extension messages
2. **Manual fill**: Some sites use custom field names - you may need to fill manually
3. **Refresh page**: Try refreshing the page and clicking fill again

### Resume Not Uploading?
1. **File size**: Ensure resume is under 5MB
2. **File format**: Supported formats are PDF, DOCX, DOC
3. **File input**: Some sites require manual file selection

### Data Not Saving?
1. **Check storage**: Open Chrome DevTools → Application → Local Storage
2. **Permissions**: Ensure extension has storage permissions
3. **Browser**: Make sure you're using a supported browser (Chrome, Edge, Brave)

## Development

### File Structure
```
job_autofill_extension/
├── manifest.json          # Extension configuration
├── popup.html             # Extension popup UI
├── popup.js               # Popup logic and data management
├── popup.css              # Popup styling
├── content.js             # Form detection and filling logic
├── content.css            # Injected styles
├── background.js          # Background service worker
├── icons/                 # Extension icons
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── README.md             # This file
```

### Building Icons
```bash
pip install Pillow
python generate_icons.py
```

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This extension is provided as-is for personal use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review browser console for errors
3. Ensure all permissions are granted

---

**Made with ❤️ for job seekers who want to save time on applications**



