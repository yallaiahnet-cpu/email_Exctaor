// Content script for JD Extractor extension

// Listen for messages from sidebar
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getPageText') {
        // Extract all text from the page
        const pageText = document.body.innerText;
        sendResponse({ text: pageText });
    }
});

// Auto-detect job description sections (optional enhancement)
function detectJobDescription() {
    const selectors = [
        'article[class*="job"]',
        '[class*="job-description"]',
        '[id*="job-description"]',
        '[class*="job-detail"]',
        'div[class*="jobDescription"]'
    ];
    
    for (const selector of selectors) {
        const element = document.querySelector(selector);
        if (element) {
            return element.innerText;
        }
    }
    
    return null;
}

