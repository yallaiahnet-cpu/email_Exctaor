// Sidebar JavaScript for JD Extractor

let currentJDId = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadSavedJDs();
});

function setupEventListeners() {
    document.getElementById('extractBtn').addEventListener('click', extractJD);
    document.getElementById('saveBtn').addEventListener('click', saveJD);
    document.getElementById('copyNoteBtn').addEventListener('click', copyNote);
    document.getElementById('newJDBtn').addEventListener('click', resetForm);
    document.getElementById('toggleView').addEventListener('click', () => showSection('savedSection'));
    document.getElementById('backToPasteBtn').addEventListener('click', () => showSection('pasteSection'));
    document.getElementById('refreshBtn').addEventListener('click', loadSavedJDs);
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
}

async function extractJD() {
    const jdText = document.getElementById('jdInput').value.trim();
    
    if (!jdText) {
        showStatus('Please paste a job description', 'error');
        return;
    }

    // Split multiple JDs by "---" or detect multiple job postings
    const jdSeparator = /---+|={3,}|\n{3,}/;
    const jdParts = jdText.split(jdSeparator).map(part => part.trim()).filter(part => part.length > 0);
    
    if (jdParts.length === 0) {
        showStatus('Please paste a job description', 'error');
        return;
    }

    // If multiple JDs detected, process them in queue
    if (jdParts.length > 1) {
        await processMultipleJDs(jdParts);
        return;
    }

    // Single JD processing
    await processSingleJD(jdParts[0], true);
}

async function processMultipleJDs(jdParts) {
    const queueContainer = document.getElementById('processingQueue');
    const queueStatus = document.getElementById('queueStatus');
    const queueProgress = document.getElementById('queueProgress');
    
    queueContainer.style.display = 'block';
    queueStatus.innerHTML = '';
    queueProgress.innerHTML = '';
    
    document.getElementById('extractBtn').disabled = true;
    document.getElementById('extractBtn').textContent = `⏳ Processing ${jdParts.length} JDs...`;
    
    const queueItems = [];
    let completedCount = 0;
    
    // Create queue items
    jdParts.forEach((jd, index) => {
        const itemId = `queue-item-${index}`;
        const item = document.createElement('div');
        item.id = itemId;
        item.className = 'queue-item processing';
        item.innerHTML = `
            <div class="queue-item-info">
                <div class="queue-item-company">JD ${index + 1} - Processing...</div>
                <div class="queue-item-status">Extracting details...</div>
            </div>
        `;
        queueStatus.appendChild(item);
        queueItems.push({ id: itemId, jd: jd, index: index });
    });
    
    // Add progress bar
    const progressBar = document.createElement('div');
    progressBar.className = 'queue-progress-bar';
    progressBar.innerHTML = '<div class="queue-progress-fill" style="width: 0%"></div>';
    queueProgress.appendChild(progressBar);
    const progressFill = progressBar.querySelector('.queue-progress-fill');
    
    // Process each JD sequentially
    for (let i = 0; i < queueItems.length; i++) {
        const item = queueItems[i];
        const queueItemEl = document.getElementById(item.id);
        
        try {
            // Update status
            queueItemEl.querySelector('.queue-item-status').textContent = 'Extracting...';
            
            // Extract JD
            const extractedData = await extractSingleJDData(item.jd);
            
            if (extractedData) {
                // Auto-save
                const jdData = {
                    id: Date.now().toString() + '-' + i,
                    recruiter_name: extractedData.recruiter_name || '',
                    company_name: extractedData.company_name || '',
                    location: extractedData.location || '',
                    key_focus: extractedData.key_focus || '',
                    linkedin_note: extractedData.linkedin_note || '',
                    date_time: new Date().toLocaleString('en-US', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit'
                    }),
                    created_at: new Date().toISOString()
                };
                
                // Save to storage
                await saveJDToStorage(jdData);
                
                // Update UI
                queueItemEl.className = 'queue-item completed';
                queueItemEl.querySelector('.queue-item-company').textContent = 
                    `JD ${i + 1} - ${extractedData.company_name || 'Extracted'}`;
                queueItemEl.querySelector('.queue-item-status').textContent = '✅ Saved';
                
                completedCount++;
                
                // Refresh saved list to show new JD immediately
                await loadSavedJDs();
                
                // Auto-switch to saved section after first JD is processed
                if (completedCount === 1) {
                    showSection('savedSection');
                }
            } else {
                throw new Error('Failed to extract JD');
            }
            
        } catch (error) {
            console.error(`Error processing JD ${i + 1}:`, error);
            queueItemEl.className = 'queue-item error';
            queueItemEl.querySelector('.queue-item-status').textContent = '❌ Error: ' + error.message;
        }
        
        // Update progress
        const progress = ((i + 1) / queueItems.length) * 100;
        progressFill.style.width = progress + '%';
    }
    
    // Show completion message
    showStatus(`Successfully processed ${completedCount} out of ${jdParts.length} JDs!`, 'success');
    
    // Reset button
    document.getElementById('extractBtn').disabled = false;
    document.getElementById('extractBtn').textContent = '✨ Extract & Generate Notes';
    
    // Clear input after processing
    setTimeout(() => {
        document.getElementById('jdInput').value = '';
        queueContainer.style.display = 'none';
    }, 3000);
}

async function processSingleJD(jdText, showResults = false) {
    showStatus('Extracting job details...', 'info');
    document.getElementById('extractBtn').disabled = true;
    document.getElementById('extractBtn').textContent = '⏳ Processing...';

    try {
        const data = await extractSingleJDData(jdText);
        
        if (!data) {
            throw new Error('Failed to extract JD');
        }

        // Populate fields
        document.getElementById('recruiterName').value = data.recruiter_name || '';
        document.getElementById('companyName').value = data.company_name || '';
        document.getElementById('location').value = data.location || '';
        document.getElementById('keyFocus').value = data.key_focus || '';
        document.getElementById('linkedInNote').value = data.linkedin_note || '';
        
        // Set current date/time
        const now = new Date();
        document.getElementById('dateTime').value = now.toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        // Show results section if requested
        if (showResults) {
            showSection('resultsSection');
        }
        
        showStatus('Job details extracted successfully!', 'success');

    } catch (error) {
        console.error('Error extracting JD:', error);
        showStatus('Error extracting job details: ' + error.message, 'error');
        
        // Fallback: Try to extract manually
        extractManually(jdText);
    } finally {
        document.getElementById('extractBtn').disabled = false;
        document.getElementById('extractBtn').textContent = '✨ Extract & Generate Notes';
    }
}

async function extractSingleJDData(jdText) {
    try {
        // Call Flask API endpoint for JD extraction
        const response = await fetch('http://localhost:5002/extract_jd', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ job_description: jdText })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        return data;
    } catch (error) {
        console.error('Error in extractSingleJDData:', error);
        // Fallback to manual extraction
        return extractManuallyData(jdText);
    }
}

function extractManuallyData(jdText) {
    // Fallback manual extraction using regex patterns
    const recruiterMatch = jdText.match(/(?:Recruiter|Contact|Hiring Manager)[:]\s*([A-Za-z\s]+)/i) ||
                          jdText.match(/([A-Z][a-z]+\s+[A-Z][a-z]+)\s*(?:@|Recruiter|Contact)/i);
    
    const companyMatch = jdText.match(/(?:Company|Organization)[:]\s*([A-Za-z\s&\.,]+)/i) ||
                        jdText.match(/([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:LLC|Inc|Corp|Tech|Solutions))/i);
    
    const locationMatch = jdText.match(/(?:Location|City)[:]\s*([A-Za-z\s,]+)/i) ||
                         jdText.match(/([A-Z][a-z]+,?\s+[A-Z]{2}(?:\s+US)?)/i);

    const recruiter_name = recruiterMatch ? recruiterMatch[1].trim() : '';
    const company_name = companyMatch ? companyMatch[1].trim() : '';
    const location = locationMatch ? locationMatch[1].trim() : '';
    const key_focus = 'Python, AI/ML, Spark/PySpark, Databricks';
    const linkedin_note = `Hi ${recruiter_name || '[Name]'}, I'm an AI Engineer with 11 years of experience. I specialize in building production AI/ML solutions using ${key_focus}. Reach me: 9733271133.`;
    
    return {
        recruiter_name,
        company_name,
        location,
        key_focus,
        linkedin_note
    };
}

function extractManually(jdText) {
    const data = extractManuallyData(jdText);
    
    document.getElementById('recruiterName').value = data.recruiter_name;
    document.getElementById('companyName').value = data.company_name;
    document.getElementById('location').value = data.location;
    document.getElementById('keyFocus').value = data.key_focus;
    document.getElementById('linkedInNote').value = data.linkedin_note;
    
    const now = new Date();
    document.getElementById('dateTime').value = now.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });

    showSection('resultsSection');
    showStatus('Manual extraction completed. Please review and edit fields.', 'info');
}

async function saveJDToStorage(jdData) {
    return new Promise((resolve) => {
        chrome.storage.local.get(['jds'], (result) => {
            const jds = result.jds || [];
            jds.push(jdData);
            chrome.storage.local.set({ jds: jds }, () => {
                resolve();
            });
        });
    });
}

function saveJD() {
    const jdData = {
        id: currentJDId || Date.now().toString(),
        recruiter_name: document.getElementById('recruiterName').value.trim(),
        company_name: document.getElementById('companyName').value.trim(),
        location: document.getElementById('location').value.trim(),
        key_focus: document.getElementById('keyFocus').value.trim(),
        linkedin_note: document.getElementById('linkedInNote').value.trim(),
        date_time: document.getElementById('dateTime').value,
        created_at: currentJDId ? undefined : new Date().toISOString(),
        updated_at: new Date().toISOString()
    };

    // Save to Chrome storage
    chrome.storage.local.get(['jds'], (result) => {
        const jds = result.jds || [];
        
        if (currentJDId) {
            // Update existing
            const index = jds.findIndex(jd => jd.id === currentJDId);
            if (index !== -1) {
                jds[index] = { ...jds[index], ...jdData };
            }
        } else {
            // Add new
            jds.push(jdData);
        }
        
        chrome.storage.local.set({ jds: jds }, () => {
            showStatus('JD saved successfully!', 'success');
            currentJDId = null;
            loadSavedJDs();
            // Auto-switch to saved section to show the new JD
            setTimeout(() => {
                showSection('savedSection');
            }, 500);
        });
    });
}

function copyNote() {
    const note = document.getElementById('linkedInNote').value;
    navigator.clipboard.writeText(note).then(() => {
        showStatus('LinkedIn note copied to clipboard!', 'success');
    }).catch(err => {
        showStatus('Failed to copy note', 'error');
    });
}

function resetForm() {
    document.getElementById('jdInput').value = '';
    document.getElementById('recruiterName').value = '';
    document.getElementById('companyName').value = '';
    document.getElementById('location').value = '';
    document.getElementById('keyFocus').value = '';
    document.getElementById('linkedInNote').value = '';
    document.getElementById('dateTime').value = '';
    currentJDId = null;
    showSection('pasteSection');
}

function loadSavedJDs() {
    return new Promise((resolve) => {
        chrome.storage.local.get(['jds'], (result) => {
            const jds = result.jds || [];
            const listContainer = document.getElementById('jdsList');
            
            if (jds.length === 0) {
                listContainer.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📋</div>
                        <p>No saved job descriptions yet.</p>
                        <p>Extract your first JD to get started!</p>
                    </div>
                `;
                resolve();
                return;
            }

            // Sort by date (newest first)
            jds.sort((a, b) => {
                const dateA = new Date(a.created_at || a.date_time || a.updated_at || 0);
                const dateB = new Date(b.created_at || b.date_time || b.updated_at || 0);
                return dateB - dateA;
            });

            listContainer.innerHTML = jds.map(jd => `
                <div class="jd-item" data-id="${jd.id}">
                    <div class="jd-header">
                        <div class="jd-company">${escapeHtml(jd.company_name || 'Unknown Company')}</div>
                        <div class="jd-date">${formatDate(jd.date_time || jd.created_at)}</div>
                    </div>
                    <div class="jd-recruiter">👤 ${escapeHtml(jd.recruiter_name || 'N/A')}</div>
                    <div class="jd-location">📍 ${escapeHtml(jd.location || 'N/A')}</div>
                    ${jd.key_focus ? `<div style="font-size: 0.85em; color: rgba(224,224,224,0.6); margin: 5px 0;">🔑 ${escapeHtml(jd.key_focus.substring(0, 100))}${jd.key_focus.length > 100 ? '...' : ''}</div>` : ''}
                    <div class="jd-actions">
                        <button class="btn-small btn-edit" onclick="editJD('${jd.id}')">✏️ Edit</button>
                        <button class="btn-small btn-copy" onclick="copyJDNote('${jd.id}')">📋 Copy Note</button>
                        <button class="btn-small btn-delete" onclick="deleteJD('${jd.id}')">🗑️ Delete</button>
                    </div>
                </div>
            `).join('');
            
            // Scroll to top to show newest JDs
            listContainer.scrollTop = 0;
            resolve();
        });
    });
}

function editJD(id) {
    chrome.storage.local.get(['jds'], (result) => {
        const jds = result.jds || [];
        const jd = jds.find(j => j.id === id);
        
        if (jd) {
            currentJDId = id;
            document.getElementById('recruiterName').value = jd.recruiter_name || '';
            document.getElementById('companyName').value = jd.company_name || '';
            document.getElementById('location').value = jd.location || '';
            document.getElementById('keyFocus').value = jd.key_focus || '';
            document.getElementById('linkedInNote').value = jd.linkedin_note || '';
            document.getElementById('dateTime').value = jd.date_time || '';
            
            showSection('resultsSection');
        }
    });
}

function copyJDNote(id) {
    chrome.storage.local.get(['jds'], (result) => {
        const jds = result.jds || [];
        const jd = jds.find(j => j.id === id);
        
        if (jd && jd.linkedin_note) {
            navigator.clipboard.writeText(jd.linkedin_note).then(() => {
                showStatus('LinkedIn note copied to clipboard!', 'success');
            });
        }
    });
}

function deleteJD(id) {
    if (!confirm('Are you sure you want to delete this JD?')) {
        return;
    }
    
    chrome.storage.local.get(['jds'], (result) => {
        const jds = result.jds || [];
        const filtered = jds.filter(j => j.id !== id);
        
        chrome.storage.local.set({ jds: filtered }, () => {
            showStatus('JD deleted successfully!', 'success');
            loadSavedJDs();
        });
    });
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch {
        return dateString;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('statusMessage');
    statusEl.textContent = message;
    statusEl.className = `status-message ${type} show`;
    
    setTimeout(() => {
        statusEl.classList.remove('show');
    }, 3000);
}

// Make functions globally available for onclick handlers
window.editJD = editJD;
window.copyJDNote = copyJDNote;
window.deleteJD = deleteJD;

