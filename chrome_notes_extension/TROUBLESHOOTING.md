# Troubleshooting - Floating Bubble Not Showing

If you can't see the floating bubble on web pages, try these steps:

## Step 1: Reload the Extension
1. Go to `chrome://extensions/`
2. Find "Personal Notes Keeper"
3. Click the **reload** button (circular arrow icon)

## Step 2: Check Console for Errors
1. Open any webpage
2. Press `F12` to open Developer Tools
3. Go to the **Console** tab
4. Look for messages like:
   - ✅ "Notes floating widget injected successfully"
   - ❌ Any error messages

## Step 3: Verify Content Script is Running
1. Open Developer Tools (F12)
2. Go to **Sources** tab
3. Look for `content.js` in the file tree
4. If you see it, the script is loading

## Step 4: Check if Widget Exists
1. Open Developer Tools (F12)
2. Go to **Console** tab
3. Type: `document.getElementById('notes-floating-widget')`
4. If it returns `null`, the widget wasn't injected
5. If it returns an element, the widget exists but might be hidden

## Step 5: Force Show Widget
If the widget exists but is hidden, try this in the console:
```javascript
const widget = document.getElementById('notes-floating-widget');
if (widget) {
    widget.style.display = 'block';
    widget.style.visibility = 'visible';
    widget.style.zIndex = '2147483647';
}
```

## Step 6: Check Page Compatibility
Some pages might block content scripts. Try:
- A simple page like `google.com`
- A new tab page
- A local HTML file

## Step 7: Reinstall Extension
If nothing works:
1. Go to `chrome://extensions/`
2. Remove the extension
3. Click "Load unpacked" again
4. Select the `chrome_notes_extension` folder

## Common Issues

### Issue: Widget appears but is behind other elements
**Solution**: The z-index should be maximum (2147483647). Check the CSS file.

### Issue: Widget doesn't appear on specific sites
**Solution**: Some sites use iframes or have strict Content Security Policies. The widget works on most sites but might not work on:
- Chrome internal pages (chrome://)
- Extension pages (chrome-extension://)
- Some banking sites with strict security

### Issue: Widget appears but is too small or invisible
**Solution**: Check if the CSS file `floating-widget.css` is loading properly in the manifest.json

## Still Not Working?
1. Check the browser console for errors
2. Make sure you're not using an ad blocker that might be blocking the widget
3. Try disabling other extensions temporarily
4. Check if the extension has the correct permissions in `chrome://extensions/`

