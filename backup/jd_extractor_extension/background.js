// Background service worker for JD Extractor extension

chrome.runtime.onInstalled.addListener(async () => {
  console.log('JD Extractor extension installed');
  try {
    // Set side panel path globally on installation
    await chrome.sidePanel.setOptions({ 
      path: 'sidebar.html',
      enabled: true
    });
    console.log('Side panel configured successfully');
  } catch (error) {
    console.error('Error setting side panel options:', error);
  }
});

// Open side panel when action button is clicked
// IMPORTANT: Must call open() directly without async operations to maintain user gesture
chrome.action.onClicked.addListener((tab) => {
  console.log('Action clicked - opening side panel for window:', tab.windowId);
  
  // Call open() immediately without any async operations before it
  // This maintains the user gesture chain
  chrome.sidePanel.open({ windowId: tab.windowId })
    .then(() => {
      console.log('✅ Side panel opened successfully');
    })
    .catch((error) => {
      console.error('❌ Error opening side panel:', error);
      console.error('Error name:', error.name);
      console.error('Error message:', error.message);
      
      // Show notification with manual instructions
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png',
        title: 'JD Extractor',
        message: 'Right-click extension icon → "Open side panel"'
      }, (notificationId) => {
        if (chrome.runtime.lastError) {
          console.error('Notification error:', chrome.runtime.lastError);
        } else {
          console.log('Notification shown:', notificationId);
        }
      });
    });
});

// Listen for messages from content script or sidebar
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'extractJD') {
    // Forward extraction request to sidebar
    chrome.runtime.sendMessage({ action: 'processJD', data: request.data });
  }
  
  if (request.action === 'saveJD') {
    // Save to local storage
    chrome.storage.local.get(['jds'], (result) => {
      const jds = result.jds || [];
      jds.push(request.data);
      chrome.storage.local.set({ jds: jds }, () => {
        sendResponse({ success: true });
      });
    });
    return true; // Keep the message channel open for async response
  }
  
  if (request.action === 'getJDs') {
    // Retrieve all saved JDs
    chrome.storage.local.get(['jds'], (result) => {
      sendResponse({ jds: result.jds || [] });
    });
    return true;
  }
  
  if (request.action === 'updateJD') {
    // Update a specific JD
    chrome.storage.local.get(['jds'], (result) => {
      const jds = result.jds || [];
      const index = jds.findIndex(jd => jd.id === request.id);
      if (index !== -1) {
        jds[index] = { ...jds[index], ...request.data };
        chrome.storage.local.set({ jds: jds }, () => {
          sendResponse({ success: true });
        });
      }
    });
    return true;
  }
  
  if (request.action === 'deleteJD') {
    // Delete a specific JD
    chrome.storage.local.get(['jds'], (result) => {
      const jds = result.jds || [];
      const filtered = jds.filter(jd => jd.id !== request.id);
      chrome.storage.local.set({ jds: filtered }, () => {
        sendResponse({ success: true });
      });
    });
    return true;
  }
});

