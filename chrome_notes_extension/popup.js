// Tab switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all tabs and buttons
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab
            button.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
            
            // If switching to notes tab, reload notes
            if (targetTab === 'notes') {
                loadNotes();
            }
        });
    });
    
    // Load notes on initial load
    loadNotes();
    
    // Note form submission
    const noteForm = document.getElementById('note-form');
    if (noteForm) {
        noteForm.addEventListener('submit', saveNote);
    }
    
    // Clear form button
    const clearBtn = document.getElementById('clear-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearForm);
    }
    
    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', filterNotes);
    }
});

// Load all notes from storage
function loadNotes() {
    chrome.storage.local.get(['notes'], function(result) {
        const notes = result.notes || [];
        // Initialize order for notes that don't have it
        notes.forEach((note, index) => {
            if (note.order === undefined) {
                note.order = index;
            }
            if (note.pinned === undefined) {
                note.pinned = false;
            }
        });
        displayNotes(notes);
    });
}

// Display notes in the list
function displayNotes(notes) {
    const notesList = document.getElementById('notes-list');
    const emptyState = document.getElementById('empty-state');
    
    if (notes.length === 0) {
        notesList.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    // Sort notes: pinned first, then by order
    notes.sort((a, b) => {
        if (a.pinned && !b.pinned) return -1;
        if (!a.pinned && b.pinned) return 1;
        return (a.order || 0) - (b.order || 0);
    });
    
    notesList.innerHTML = notes.map((note, displayIndex) => {
        const date = new Date(note.date);
        const formattedDate = date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const tagsHtml = note.tags && note.tags.length > 0 
            ? `<div class="note-tags">${note.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}</div>`
            : '';
        
        const pinnedClass = note.pinned ? 'pinned' : '';
        const pinnedIcon = note.pinned ? '📌' : '';
        
        return `
            <div class="note-item ${pinnedClass}" data-note-id="${note.id}">
                <div class="note-drag-handle" title="Drag to reorder" draggable="true">⋮⋮</div>
                <div class="note-header">
                    <div class="note-title">
                        <span class="pin-indicator">${pinnedIcon}</span>
                        ${escapeHtml(note.title)}
                    </div>
                    <div class="note-date">${formattedDate}</div>
                </div>
                <div class="note-content-preview">${escapeHtml(note.content)}</div>
                <div class="note-content-full" style="display: none;">${escapeHtml(note.content)}</div>
                ${tagsHtml}
                <div class="note-actions" style="display: none;">
                    <button class="btn-small btn-copy" onclick="copyNote('${note.id}', this)" title="Copy Note">
                        📋 Copy
                    </button>
                    <button class="btn-small btn-pin" onclick="togglePin('${note.id}')" title="${note.pinned ? 'Unpin' : 'Pin'}">
                        ${note.pinned ? '📌 Unpin' : '📌 Pin'}
                    </button>
                    <button class="btn-small btn-edit" onclick="editNote('${note.id}')">✏️ Edit</button>
                    <button class="btn-small btn-delete" onclick="deleteNote('${note.id}')">🗑️ Delete</button>
                </div>
            </div>
        `;
    }).join('');
    
    // Initialize drag and drop
    initializeDragAndDrop();
    
    // Add click handlers for expanding/collapsing notes
    notesList.querySelectorAll('.note-item').forEach(item => {
        let isSelecting = false;
        let mouseDownTime = 0;
        let mouseDownX = 0;
        let mouseDownY = 0;
        
        // Track mouse down
        item.addEventListener('mousedown', function(e) {
            if (e.target.classList.contains('btn-small') || 
                e.target.classList.contains('note-drag-handle') ||
                e.target.closest('.note-drag-handle') ||
                e.target.closest('.btn-small') ||
                e.target.closest('.note-content-full') ||
                e.target.closest('.note-content-preview')) {
                return;
            }
            mouseDownTime = Date.now();
            mouseDownX = e.clientX;
            mouseDownY = e.clientY;
        });
        
        // Track mouse move to detect text selection
        item.addEventListener('mousemove', function(e) {
            if (e.buttons === 1) {
                const deltaX = Math.abs(e.clientX - mouseDownX);
                const deltaY = Math.abs(e.clientY - mouseDownY);
                if (deltaX > 3 || deltaY > 3) {
                    isSelecting = true;
                }
            }
        });
        
        item.addEventListener('click', function(e) {
            // Don't expand if clicking on buttons, drag handle, or content areas
            if (e.target.classList.contains('btn-small') || 
                e.target.classList.contains('note-drag-handle') ||
                e.target.closest('.note-drag-handle') ||
                e.target.closest('.btn-small') ||
                e.target.closest('.note-content-full') ||
                e.target.closest('.note-content-preview')) {
                return;
            }
            
            // Don't expand if user was selecting text
            if (isSelecting) {
                isSelecting = false;
                return;
            }
            
            // Check if text is selected
            const selection = window.getSelection();
            if (selection && selection.toString().length > 0) {
                return;
            }
            
            const noteId = this.getAttribute('data-note-id');
            chrome.storage.local.get(['notes'], function(result) {
                const notes = result.notes || [];
                const note = notes.find(n => n.id.toString() === noteId);
                if (!note) return;
                
                const isExpanded = this.classList.contains('expanded');
                
                if (isExpanded) {
                    // Collapse
                    this.classList.remove('expanded');
                    const preview = this.querySelector('.note-content-preview');
                    const fullContent = this.querySelector('.note-content-full');
                    if (preview) preview.style.display = 'block';
                    if (fullContent) fullContent.style.display = 'none';
                    this.querySelector('.note-actions').style.display = 'none';
                } else {
                    // Expand - show full content
                    this.classList.add('expanded');
                    const preview = this.querySelector('.note-content-preview');
                    const fullContent = this.querySelector('.note-content-full');
                    if (preview) preview.style.display = 'none';
                    if (fullContent) fullContent.style.display = 'block';
                    
                    this.querySelector('.note-actions').style.display = 'flex';
                }
            });
        });
        
        // Reset selection flag on mouse up
        item.addEventListener('mouseup', function() {
            setTimeout(() => {
                isSelecting = false;
            }, 100);
        });
    });
}

// Initialize drag and drop functionality (only from drag handle)
function initializeDragAndDrop() {
    const notesList = document.getElementById('notes-list');
    let draggedElement = null;
    let draggedItem = null;
    
    // Attach drag events to drag handles only
    notesList.querySelectorAll('.note-drag-handle').forEach(handle => {
        const item = handle.closest('.note-item');
        
        handle.addEventListener('dragstart', function(e) {
            draggedItem = item;
            draggedElement = item;
            item.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', ''); // Required for drag to work
        });
        
        handle.addEventListener('dragend', function(e) {
            if (item) item.classList.remove('dragging');
            notesList.querySelectorAll('.note-item').forEach(note => {
                note.classList.remove('drag-over-top', 'drag-over-bottom');
            });
            draggedElement = null;
            draggedItem = null;
        });
    });
    
    // Attach drop events to items
    notesList.querySelectorAll('.note-item').forEach(item => {
        item.addEventListener('dragover', function(e) {
            if (!draggedItem || this === draggedItem) return;
            
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            
            const rect = this.getBoundingClientRect();
            const midpoint = rect.top + rect.height / 2;
            
            if (e.clientY < midpoint) {
                this.classList.add('drag-over-top');
                this.classList.remove('drag-over-bottom');
            } else {
                this.classList.add('drag-over-bottom');
                this.classList.remove('drag-over-top');
            }
        });
        
        item.addEventListener('dragleave', function(e) {
            this.classList.remove('drag-over-top', 'drag-over-bottom');
        });
        
        item.addEventListener('drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (draggedItem && this !== draggedItem) {
                const draggedId = draggedItem.getAttribute('data-note-id');
                const targetId = this.getAttribute('data-note-id');
                
                reorderNotes(draggedId, targetId, e.clientY < this.getBoundingClientRect().top + this.getBoundingClientRect().height / 2);
            }
            
            this.classList.remove('drag-over-top', 'drag-over-bottom');
        });
    });
}

// Reorder notes
function reorderNotes(draggedId, targetId, insertBefore) {
    chrome.storage.local.get(['notes'], function(result) {
        const notes = result.notes || [];
        
        const draggedIndex = notes.findIndex(n => n.id.toString() === draggedId);
        const targetIndex = notes.findIndex(n => n.id.toString() === targetId);
        
        if (draggedIndex === -1 || targetIndex === -1) return;
        
        // Separate pinned and unpinned notes
        const pinnedNotes = notes.filter(n => n.pinned);
        const unpinnedNotes = notes.filter(n => !n.pinned);
        
        // Determine which list we're working with
        const draggedNote = notes[draggedIndex];
        const targetNote = notes[targetIndex];
        
        if (draggedNote.pinned && targetNote.pinned) {
            // Reordering within pinned notes
            const pinnedIndex = pinnedNotes.findIndex(n => n.id.toString() === draggedId);
            const targetPinnedIndex = pinnedNotes.findIndex(n => n.id.toString() === targetId);
            
            pinnedNotes.splice(pinnedIndex, 1);
            const newIndex = insertBefore ? targetPinnedIndex : targetPinnedIndex + 1;
            pinnedNotes.splice(newIndex > pinnedIndex ? newIndex - 1 : newIndex, 0, draggedNote);
        } else if (!draggedNote.pinned && !targetNote.pinned) {
            // Reordering within unpinned notes
            const unpinnedIndex = unpinnedNotes.findIndex(n => n.id.toString() === draggedId);
            const targetUnpinnedIndex = unpinnedNotes.findIndex(n => n.id.toString() === targetId);
            
            unpinnedNotes.splice(unpinnedIndex, 1);
            const newIndex = insertBefore ? targetUnpinnedIndex : targetUnpinnedIndex + 1;
            unpinnedNotes.splice(newIndex > unpinnedIndex ? newIndex - 1 : newIndex, 0, draggedNote);
        }
        
        // Update order values
        pinnedNotes.forEach((note, index) => {
            note.order = index;
        });
        unpinnedNotes.forEach((note, index) => {
            note.order = index;
        });
        
        // Combine notes
        const reorderedNotes = [...pinnedNotes, ...unpinnedNotes];
        
        chrome.storage.local.set({ notes: reorderedNotes }, function() {
            loadNotes();
        });
    });
}

// Toggle pin status
function togglePin(noteId) {
    chrome.storage.local.get(['notes'], function(result) {
        const notes = result.notes || [];
        const noteIndex = notes.findIndex(n => n.id.toString() === noteId);
        
        if (noteIndex === -1) return;
        
        notes[noteIndex].pinned = !notes[noteIndex].pinned;
        
        // If pinning, move to top of its category and update order
        if (notes[noteIndex].pinned) {
            const pinnedCount = notes.filter(n => n.pinned).length - 1;
            notes[noteIndex].order = pinnedCount;
        } else {
            const unpinnedCount = notes.filter(n => !n.pinned).length - 1;
            notes[noteIndex].order = unpinnedCount;
        }
        
        chrome.storage.local.set({ notes: notes }, function() {
            loadNotes();
        });
    });
}

// Get notes synchronously (helper function)
function getNotesSync() {
    // This is a workaround - we'll use async version in practice
    let notes = [];
    chrome.storage.local.get(['notes'], function(result) {
        notes = result.notes || [];
    });
    return notes;
}

// Save a new note
function saveNote(e) {
    e.preventDefault();
    
    const title = document.getElementById('note-title').value.trim();
    const content = document.getElementById('note-content').value.trim();
    const tagsInput = document.getElementById('note-tags').value.trim();
    
    if (!title || !content) {
        alert('Please fill in both title and content!');
        return;
    }
    
    const tags = tagsInput 
        ? tagsInput.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)
        : [];
    
    chrome.storage.local.get(['notes'], function(result) {
        const notes = result.notes || [];
        const unpinnedCount = notes.filter(n => !n.pinned).length;
        
        const newNote = {
            id: Date.now(),
            title: title,
            content: content,
            tags: tags,
            date: new Date().toISOString(),
            pinned: false,
            order: unpinnedCount
        };
        
        notes.push(newNote);
        
        chrome.storage.local.set({ notes: notes }, function() {
            clearForm();
            // Switch to notes tab and reload
            document.querySelector('[data-tab="notes"]').click();
            loadNotes();
        });
    });
}

// Edit a note
function editNote(noteId) {
    chrome.storage.local.get(['notes'], function(result) {
        const notes = result.notes || [];
        const note = notes.find(n => n.id.toString() === noteId);
        
        if (note) {
            // Fill form with note data
            document.getElementById('note-title').value = note.title;
            document.getElementById('note-content').value = note.content;
            document.getElementById('note-tags').value = note.tags ? note.tags.join(', ') : '';
            
            // Switch to add tab
            document.querySelector('[data-tab="add"]').click();
            
            // Change form submit to update instead of create
            const form = document.getElementById('note-form');
            form.onsubmit = function(e) {
                e.preventDefault();
                updateNote(noteId, e);
            };
            
            // Add update button
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.textContent = '💾 Update Note';
        }
    });
}

// Update an existing note
function updateNote(noteId, e) {
    e.preventDefault();
    
    const title = document.getElementById('note-title').value.trim();
    const content = document.getElementById('note-content').value.trim();
    const tagsInput = document.getElementById('note-tags').value.trim();
    
    if (!title || !content) {
        alert('Please fill in both title and content!');
        return;
    }
    
    const tags = tagsInput 
        ? tagsInput.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)
        : [];
    
    chrome.storage.local.get(['notes'], function(result) {
        const notes = result.notes || [];
        const noteIndex = notes.findIndex(n => n.id.toString() === noteId);
        
        if (noteIndex === -1) return;
        
        notes[noteIndex] = {
            ...notes[noteIndex],
            title: title,
            content: content,
            tags: tags,
            date: new Date().toISOString()
        };
        
        chrome.storage.local.set({ notes: notes }, function() {
            clearForm();
            // Reset form submit handler
            const form = document.getElementById('note-form');
            form.onsubmit = saveNote;
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.textContent = '💾 Save Note';
            
            // Switch to notes tab and reload
            document.querySelector('[data-tab="notes"]').click();
            loadNotes();
        });
    });
}

// Delete a note
function deleteNote(noteId) {
    if (confirm('Are you sure you want to delete this note?')) {
        chrome.storage.local.get(['notes'], function(result) {
            const notes = result.notes || [];
            const noteIndex = notes.findIndex(n => n.id.toString() === noteId);
            if (noteIndex !== -1) {
                notes.splice(noteIndex, 1);
                // Reorder remaining notes
                const pinnedNotes = notes.filter(n => n.pinned);
                const unpinnedNotes = notes.filter(n => !n.pinned);
                pinnedNotes.forEach((note, index) => {
                    note.order = index;
                });
                unpinnedNotes.forEach((note, index) => {
                    note.order = index;
                });
            }
            
            chrome.storage.local.set({ notes: notes }, function() {
                loadNotes();
            });
        });
    }
}

// Clear form
function clearForm() {
    document.getElementById('note-form').reset();
    const form = document.getElementById('note-form');
    form.onsubmit = saveNote;
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.textContent = '💾 Save Note';
}

// Filter notes by search query
function filterNotes() {
    const searchQuery = document.getElementById('search-input').value.toLowerCase();
    
    chrome.storage.local.get(['notes'], function(result) {
        const notes = result.notes || [];
        
        if (!searchQuery) {
            displayNotes(notes);
            return;
        }
        
        const filteredNotes = notes.filter(note => {
            const titleMatch = note.title.toLowerCase().includes(searchQuery);
            const contentMatch = note.content.toLowerCase().includes(searchQuery);
            const tagsMatch = note.tags && note.tags.some(tag => 
                tag.toLowerCase().includes(searchQuery)
            );
            
            return titleMatch || contentMatch || tagsMatch;
        });
        
        displayNotes(filteredNotes);
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Copy note content to clipboard
function copyNote(noteId, buttonElement) {
    chrome.storage.local.get(['notes'], function(result) {
        const notes = result.notes || [];
        const note = notes.find(n => n.id.toString() === noteId);
        
        if (!note) return;
        
        // Create copy text with title and content
        const copyText = `Title: ${note.title}\n\n${note.content}${note.tags && note.tags.length > 0 ? `\n\nTags: ${note.tags.join(', ')}` : ''}`;
        
        // Use modern clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(copyText).then(function() {
                showCopyFeedback(buttonElement);
            }).catch(function(err) {
                console.error('Failed to copy:', err);
                fallbackCopyTextToClipboard(copyText, buttonElement);
            });
        } else {
            fallbackCopyTextToClipboard(copyText, buttonElement);
        }
    });
}

// Show copy feedback
function showCopyFeedback(button) {
    if (!button) return;
    const originalText = button.textContent;
    const originalBg = button.style.background;
    button.textContent = '✅ Copied!';
    button.style.background = '#4caf50';
    setTimeout(function() {
        button.textContent = originalText;
        button.style.background = originalBg;
    }, 2000);
}

// Fallback copy method
function fallbackCopyTextToClipboard(text, buttonElement) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopyFeedback(buttonElement);
        } else {
            alert('Failed to copy. Please select and copy manually.');
        }
    } catch (err) {
        console.error('Fallback copy failed:', err);
        alert('Failed to copy. Please select and copy manually.');
    }
    
    document.body.removeChild(textArea);
}

// Make functions globally available for onclick handlers
window.editNote = editNote;
window.deleteNote = deleteNote;
window.togglePin = togglePin;
window.copyNote = copyNote;
