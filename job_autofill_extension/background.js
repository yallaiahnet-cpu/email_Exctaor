// Background service worker for job autofill extension

// Listen for installation
chrome.runtime.onInstalled.addListener(() => {
    console.log('Job Application Auto-Fill extension installed');
});

// Handle messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'uploadResume') {
        // Handle resume upload if needed
        sendResponse({ success: true });
    }
    return true;
});



