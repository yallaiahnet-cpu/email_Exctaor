// Content script to inject floating notes widget
(function() {
    'use strict';
    
    // Wait for page to be ready
    function initWidget() {
        // Check if widget already exists
        if (document.getElementById('notes-floating-widget')) {
            return;
        }
        
        // Ensure body exists
        if (!document.body) {
            setTimeout(initWidget, 100);
            return;
        }
    
    // Create floating widget container
    const widget = document.createElement('div');
    widget.id = 'notes-floating-widget';
    
    // Create floating bubble button
    const bubble = document.createElement('div');
    bubble.id = 'notes-floating-bubble';
    bubble.innerHTML = '📝';
    bubble.title = 'Personal Notes';
    
    // Create notification badge
    const badge = document.createElement('div');
    badge.id = 'notes-badge';
    badge.textContent = '0';
    bubble.appendChild(badge);
    
    // Create floating panel
    const panel = document.createElement('div');
    panel.id = 'notes-floating-panel';
    
    // Panel header
    const header = document.createElement('div');
    header.id = 'notes-panel-header';
    header.innerHTML = `
        <h2>📝 Personal Notes</h2>
        <button id="notes-close-btn">×</button>
    `;
    
    // Panel tabs
    const tabs = document.createElement('div');
    tabs.id = 'notes-panel-tabs';
    tabs.innerHTML = `
        <button class="notes-tab-btn active" data-tab="list">My Notes</button>
        <button class="notes-tab-btn" data-tab="add">Add Note</button>
    `;
    
    // Panel content
    const content = document.createElement('div');
    content.id = 'notes-panel-content';
    
    // Notes list view
    const listView = document.createElement('div');
    listView.id = 'notes-list-view';
    listView.innerHTML = `
        <div id="notes-panel-search">
            <input type="text" id="notes-search-input" placeholder="🔍 Search notes...">
        </div>
        <div id="notes-panel-list"></div>
        <div id="notes-panel-empty" style="display: none;">
            <p>No notes yet. Click "Add Note" to create your first note!</p>
        </div>
    `;
    
    // Add note form view
    const formView = document.createElement('div');
    formView.id = 'notes-panel-form';
    formView.innerHTML = `
        <form id="notes-add-form">
            <div class="notes-form-group">
                <label for="notes-form-title">Title:</label>
                <input type="text" id="notes-form-title" placeholder="Enter note title..." required>
            </div>
            <div class="notes-form-group">
                <label for="notes-form-content">Content:</label>
                <textarea id="notes-form-content" placeholder="Write your note here..." required></textarea>
            </div>
            <div class="notes-form-group">
                <label for="notes-form-tags">Tags (comma separated):</label>
                <input type="text" id="notes-form-tags" placeholder="e.g., work, personal, ideas">
            </div>
            <div class="notes-form-actions">
                <button type="submit" class="notes-form-btn notes-form-btn-primary">💾 Save</button>
                <button type="button" class="notes-form-btn notes-form-btn-secondary" id="notes-form-clear">Clear</button>
            </div>
        </form>
    `;
    
    content.appendChild(listView);
    content.appendChild(formView);
    
    // Assemble panel
    panel.appendChild(header);
    panel.appendChild(tabs);
    panel.appendChild(content);
    
    // Assemble widget
    widget.appendChild(bubble);
    widget.appendChild(panel);
    
        // Inject into page
        try {
            document.body.appendChild(widget);
            console.log('✅ Notes floating widget injected successfully');
            
            // Force visibility
            widget.style.display = 'block';
            widget.style.visibility = 'visible';
            bubble.style.display = 'flex';
            bubble.style.visibility = 'visible';
            
            // Verify it's visible
            setTimeout(() => {
                const checkWidget = document.getElementById('notes-floating-widget');
                if (checkWidget) {
                    console.log('✅ Widget confirmed visible:', checkWidget.offsetWidth, 'x', checkWidget.offsetHeight);
                } else {
                    console.error('❌ Widget not found after injection');
                }
            }, 500);
        } catch (error) {
            console.error('❌ Error injecting widget:', error);
        }
    
    // Widget functionality
    let isPanelOpen = false;
    let currentTab = 'list';
    
    // Toggle panel
    bubble.addEventListener('click', function(e) {
        e.stopPropagation();
        togglePanel();
    });
    
    // Close button
    const closeBtn = document.getElementById('notes-close-btn');
    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        closePanel();
    });
    
    // Tab switching
    tabs.querySelectorAll('.notes-tab-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const tab = this.getAttribute('data-tab');
            switchTab(tab);
        });
    });
    
    // Click outside to close
    document.addEventListener('click', function(e) {
        if (isPanelOpen && !panel.contains(e.target) && !bubble.contains(e.target)) {
            closePanel();
        }
    });
    
    // Prevent clicks inside panel from closing
    panel.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    function togglePanel() {
        if (isPanelOpen) {
            closePanel();
        } else {
            openPanel();
        }
    }
    
    function openPanel() {
        panel.classList.add('show');
        bubble.classList.add('active');
        isPanelOpen = true;
        loadNotes();
    }
    
    function closePanel() {
        panel.classList.remove('show');
        bubble.classList.remove('active');
        isPanelOpen = false;
    }
    
    function switchTab(tab) {
        currentTab = tab;
        
        // Update tab buttons
        tabs.querySelectorAll('.notes-tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.getAttribute('data-tab') === tab) {
                btn.classList.add('active');
            }
        });
        
        // Show/hide views
        if (tab === 'list') {
            listView.style.display = 'block';
            formView.classList.remove('show');
            loadNotes();
        } else {
            listView.style.display = 'none';
            formView.classList.add('show');
        }
    }
    
    // Load notes from storage
    function loadNotes() {
        chrome.storage.local.get(['notes'], function(result) {
            const notes = result.notes || [];
            // Initialize order and pinned for notes that don't have it
            notes.forEach((note, index) => {
                if (note.order === undefined) {
                    note.order = index;
                }
                if (note.pinned === undefined) {
                    note.pinned = false;
                }
            });
            displayNotes(notes);
            updateBadge(notes.length);
        });
    }
    
    // Display notes
    function displayNotes(notes) {
        const list = document.getElementById('notes-panel-list');
        const empty = document.getElementById('notes-panel-empty');
        const searchQuery = document.getElementById('notes-search-input').value.toLowerCase();
        
        // Filter notes
        let filteredNotes = notes;
        if (searchQuery) {
            filteredNotes = notes.filter(note => {
                const titleMatch = note.title.toLowerCase().includes(searchQuery);
                const contentMatch = note.content.toLowerCase().includes(searchQuery);
                const tagsMatch = note.tags && note.tags.some(tag => 
                    tag.toLowerCase().includes(searchQuery)
                );
                return titleMatch || contentMatch || tagsMatch;
            });
        }
        
        // Sort notes: pinned first, then by order
        filteredNotes.sort((a, b) => {
            if (a.pinned && !b.pinned) return -1;
            if (!a.pinned && b.pinned) return 1;
            return (a.order || 0) - (b.order || 0);
        });
        
        if (filteredNotes.length === 0) {
            list.innerHTML = '';
            empty.style.display = 'block';
            return;
        }
        
        empty.style.display = 'none';
        
        list.innerHTML = filteredNotes.map((note, index) => {
            const date = new Date(note.date);
            const formattedDate = date.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            const tagsHtml = note.tags && note.tags.length > 0 
                ? `<div class="notes-panel-item-tags">${note.tags.map(tag => 
                    `<span class="notes-panel-tag">${tag}</span>`
                ).join('')}</div>`
                : '';
            
            const pinnedClass = note.pinned ? 'notes-panel-item-pinned' : '';
            const pinnedIcon = note.pinned ? '📌 ' : '';
            
            return `
                <div class="notes-panel-item ${pinnedClass}" data-note-id="${note.id}">
                    <div class="notes-panel-drag-handle" title="Drag to reorder" draggable="true">⋮⋮</div>
                    <div class="notes-panel-item-title">${pinnedIcon}${escapeHtml(note.title)}</div>
                    <div class="notes-panel-item-content-preview">${escapeHtml(note.content)}</div>
                    <div class="notes-panel-item-content-full" style="display: none;">${escapeHtml(note.content)}</div>
                    <div class="notes-panel-item-date">${formattedDate}</div>
                    ${tagsHtml}
                    <div class="notes-panel-item-actions" style="display: none;">
                        <button class="notes-panel-btn notes-panel-btn-copy" onclick="window.copyNoteFloating('${note.id}', this)" title="Copy Note">
                            📋 Copy
                        </button>
                        <button class="notes-panel-btn notes-panel-btn-pin" onclick="window.togglePinFloating('${note.id}')" title="${note.pinned ? 'Unpin' : 'Pin'}">
                            ${note.pinned ? '📌 Unpin' : '📌 Pin'}
                        </button>
                        <button class="notes-panel-btn notes-panel-btn-edit" onclick="window.editNoteFloating('${note.id}')" title="Edit Note">
                            ✏️ Edit
                        </button>
                        <button class="notes-panel-btn notes-panel-btn-delete" onclick="window.deleteNoteFloating('${note.id}')" title="Delete Note">
                            🗑️ Delete
                        </button>
                    </div>
                </div>
            `;
        }).join('');
        
        // Initialize drag and drop
        initializeDragAndDropFloating(list, filteredNotes);
        
        // Add click handlers
        list.querySelectorAll('.notes-panel-item').forEach(item => {
            let isSelecting = false;
            let mouseDownTime = 0;
            let mouseDownX = 0;
            let mouseDownY = 0;
            
            // Track mouse down
            item.addEventListener('mousedown', function(e) {
                if (e.target.classList.contains('notes-panel-btn') || 
                    e.target.classList.contains('notes-panel-drag-handle') ||
                    e.target.closest('.notes-panel-drag-handle') ||
                    e.target.closest('.notes-panel-btn') ||
                    e.target.closest('.notes-panel-item-content-full') ||
                    e.target.closest('.notes-panel-item-content-preview')) {
                    // Allow text selection in content areas
                    return;
                }
                mouseDownTime = Date.now();
                mouseDownX = e.clientX;
                mouseDownY = e.clientY;
            });
            
            // Track mouse move to detect text selection
            item.addEventListener('mousemove', function(e) {
                if (e.buttons === 1) { // Mouse button is pressed
                    const deltaX = Math.abs(e.clientX - mouseDownX);
                    const deltaY = Math.abs(e.clientY - mouseDownY);
                    if (deltaX > 3 || deltaY > 3) { // User is dragging (selecting text)
                        isSelecting = true;
                    }
                }
            });
            
            // Handle click (but not text selection)
            item.addEventListener('click', function(e) {
                // Don't expand if clicking on buttons, drag handle, or content areas
                if (e.target.classList.contains('notes-panel-btn') || 
                    e.target.classList.contains('notes-panel-drag-handle') ||
                    e.target.closest('.notes-panel-drag-handle') ||
                    e.target.closest('.notes-panel-btn') ||
                    e.target.closest('.notes-panel-item-content-full') ||
                    e.target.closest('.notes-panel-item-content-preview')) {
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
                    return; // User is selecting text, don't expand
                }
                
                const noteId = parseInt(this.getAttribute('data-note-id'));
                const note = notes.find(n => n.id === noteId);
                if (!note) return;
                
                const isExpanded = this.classList.contains('notes-panel-expanded');
                const actions = this.querySelector('.notes-panel-item-actions');
                const preview = this.querySelector('.notes-panel-item-content-preview');
                const fullContent = this.querySelector('.notes-panel-item-content-full');
                
                if (isExpanded) {
                    // Collapse
                    this.classList.remove('notes-panel-expanded');
                    if (actions) actions.style.display = 'none';
                    if (preview) preview.style.display = 'block';
                    if (fullContent) fullContent.style.display = 'none';
                } else {
                    // Expand - show full content
                    this.classList.add('notes-panel-expanded');
                    if (actions) actions.style.display = 'flex';
                    if (preview) preview.style.display = 'none';
                    if (fullContent) fullContent.style.display = 'block';
                }
            });
            
            // Reset selection flag on mouse up
            item.addEventListener('mouseup', function() {
                setTimeout(() => {
                    isSelecting = false;
                }, 100);
            });
        });
    }
    
    // Initialize drag and drop for floating widget (only from drag handle)
    function initializeDragAndDropFloating(list, notes) {
        let draggedElement = null;
        let draggedItem = null;
        
        // Attach drag events to drag handles only
        list.querySelectorAll('.notes-panel-drag-handle').forEach(handle => {
            const item = handle.closest('.notes-panel-item');
            
            handle.addEventListener('dragstart', function(e) {
                draggedItem = item;
                draggedElement = item;
                item.classList.add('notes-panel-dragging');
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/plain', ''); // Required for drag to work
            });
            
            handle.addEventListener('dragend', function(e) {
                if (item) item.classList.remove('notes-panel-dragging');
                list.querySelectorAll('.notes-panel-item').forEach(note => {
                    note.classList.remove('notes-panel-drag-over-top', 'notes-panel-drag-over-bottom');
                });
                draggedElement = null;
                draggedItem = null;
            });
        });
        
        // Attach drop events to items
        list.querySelectorAll('.notes-panel-item').forEach(item => {
            item.addEventListener('dragover', function(e) {
                if (!draggedItem || this === draggedItem) return;
                
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                
                const rect = this.getBoundingClientRect();
                const midpoint = rect.top + rect.height / 2;
                
                if (e.clientY < midpoint) {
                    this.classList.add('notes-panel-drag-over-top');
                    this.classList.remove('notes-panel-drag-over-bottom');
                } else {
                    this.classList.add('notes-panel-drag-over-bottom');
                    this.classList.remove('notes-panel-drag-over-top');
                }
            });
            
            item.addEventListener('dragleave', function(e) {
                this.classList.remove('notes-panel-drag-over-top', 'notes-panel-drag-over-bottom');
            });
            
            item.addEventListener('drop', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                if (draggedItem && this !== draggedItem) {
                    const draggedId = draggedItem.getAttribute('data-note-id');
                    const targetId = this.getAttribute('data-note-id');
                    
                    reorderNotesFloating(draggedId, targetId, e.clientY < this.getBoundingClientRect().top + this.getBoundingClientRect().height / 2);
                }
                
                this.classList.remove('notes-panel-drag-over-top', 'notes-panel-drag-over-bottom');
            });
        });
    }
    
    // Reorder notes in floating widget
    function reorderNotesFloating(draggedId, targetId, insertBefore) {
        chrome.storage.local.get(['notes'], function(result) {
            const notes = result.notes || [];
            
            const draggedIndex = notes.findIndex(n => n.id.toString() === draggedId);
            const targetIndex = notes.findIndex(n => n.id.toString() === targetId);
            
            if (draggedIndex === -1 || targetIndex === -1) return;
            
            const pinnedNotes = notes.filter(n => n.pinned);
            const unpinnedNotes = notes.filter(n => !n.pinned);
            
            const draggedNote = notes[draggedIndex];
            const targetNote = notes[targetIndex];
            
            if (draggedNote.pinned && targetNote.pinned) {
                const pinnedIndex = pinnedNotes.findIndex(n => n.id.toString() === draggedId);
                const targetPinnedIndex = pinnedNotes.findIndex(n => n.id.toString() === targetId);
                
                pinnedNotes.splice(pinnedIndex, 1);
                const newIndex = insertBefore ? targetPinnedIndex : targetPinnedIndex + 1;
                pinnedNotes.splice(newIndex > pinnedIndex ? newIndex - 1 : newIndex, 0, draggedNote);
            } else if (!draggedNote.pinned && !targetNote.pinned) {
                const unpinnedIndex = unpinnedNotes.findIndex(n => n.id.toString() === draggedId);
                const targetUnpinnedIndex = unpinnedNotes.findIndex(n => n.id.toString() === targetId);
                
                unpinnedNotes.splice(unpinnedIndex, 1);
                const newIndex = insertBefore ? targetUnpinnedIndex : targetUnpinnedIndex + 1;
                unpinnedNotes.splice(newIndex > unpinnedIndex ? newIndex - 1 : newIndex, 0, draggedNote);
            }
            
            pinnedNotes.forEach((note, index) => {
                note.order = index;
            });
            unpinnedNotes.forEach((note, index) => {
                note.order = index;
            });
            
            const reorderedNotes = [...pinnedNotes, ...unpinnedNotes];
            
            chrome.storage.local.set({ notes: reorderedNotes }, function() {
                loadNotes();
            });
        });
    }
    
    // Toggle pin in floating widget
    window.togglePinFloating = function(noteId) {
        chrome.storage.local.get(['notes'], function(result) {
            const notes = result.notes || [];
            const noteIndex = notes.findIndex(n => n.id.toString() === noteId);
            
            if (noteIndex === -1) return;
            
            notes[noteIndex].pinned = !notes[noteIndex].pinned;
            
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
    };
    
    // Edit note in floating widget
    window.editNoteFloating = function(noteId) {
        chrome.storage.local.get(['notes'], function(result) {
            const notes = result.notes || [];
            const note = notes.find(n => n.id.toString() === noteId);
            
            if (!note) return;
            
            // Fill form with note data
            const titleInput = document.getElementById('notes-form-title');
            const contentInput = document.getElementById('notes-form-content');
            const tagsInput = document.getElementById('notes-form-tags');
            
            if (titleInput) titleInput.value = note.title;
            if (contentInput) contentInput.value = note.content;
            if (tagsInput) tagsInput.value = note.tags ? note.tags.join(', ') : '';
            
            // Switch to add tab
            switchTab('add');
            
            // Update form submit handler
            const form = document.getElementById('notes-add-form');
            if (form) {
                form.onsubmit = function(e) {
                    e.preventDefault();
                    updateNoteFloating(noteId, e);
                };
                
                // Update submit button text
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) submitBtn.textContent = '💾 Update Note';
            }
        });
    };
    
    // Update note in floating widget
    function updateNoteFloating(noteId, e) {
        e.preventDefault();
        
        const title = document.getElementById('notes-form-title').value.trim();
        const content = document.getElementById('notes-form-content').value.trim();
        const tagsInput = document.getElementById('notes-form-tags').value.trim();
        
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
                // Reset form
                const form = document.getElementById('notes-add-form');
                if (form) {
                    form.reset();
                    form.onsubmit = function(e) {
                        e.preventDefault();
                        saveNote();
                    };
                    const submitBtn = form.querySelector('button[type="submit"]');
                    if (submitBtn) submitBtn.textContent = '💾 Save';
                }
                
                // Switch back to list and reload
                switchTab('list');
                loadNotes();
            });
        });
    }
    
    // Copy note content to clipboard
    window.copyNoteFloating = function(noteId, buttonElement) {
        chrome.storage.local.get(['notes'], function(result) {
            const notes = result.notes || [];
            const note = notes.find(n => n.id.toString() === noteId);
            
            if (!note) return;
            
            // Create copy text with title and content
            const copyText = `Title: ${note.title}\n\n${note.content}${note.tags && note.tags.length > 0 ? `\n\nTags: ${note.tags.join(', ')}` : ''}`;
            
            // Use modern clipboard API
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(copyText).then(function() {
                    // Show feedback
                    showCopyFeedback(buttonElement);
                }).catch(function(err) {
                    console.error('Failed to copy:', err);
                    // Fallback to old method
                    fallbackCopyTextToClipboard(copyText, buttonElement);
                });
            } else {
                // Fallback for older browsers
                fallbackCopyTextToClipboard(copyText, buttonElement);
            }
        });
    };
    
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
    
    // Delete note in floating widget
    window.deleteNoteFloating = function(noteId) {
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
    };
    
    // Show note details (simple alert for now, can be enhanced)
    function showNoteDetails(note) {
        const date = new Date(note.date);
        const formattedDate = date.toLocaleDateString('en-US', { 
            month: 'long', 
            day: 'numeric', 
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const tags = note.tags && note.tags.length > 0 ? note.tags.join(', ') : 'No tags';
        
        alert(`Title: ${note.title}\n\nContent:\n${note.content}\n\nTags: ${tags}\n\nDate: ${formattedDate}`);
    }
    
    // Update badge
    function updateBadge(count) {
        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.classList.add('show');
        } else {
            badge.classList.remove('show');
        }
    }
    
    // Search functionality
    const searchInput = document.getElementById('notes-search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            loadNotes();
        });
    }
    
    // Form submission
    const form = document.getElementById('notes-add-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            saveNote();
        });
    }
    
    // Clear form
    const clearBtn = document.getElementById('notes-form-clear');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            form.reset();
            // Reset form to create mode
            form.onsubmit = function(e) {
                e.preventDefault();
                saveNote();
            };
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.textContent = '💾 Save';
        });
    }
    
    // Save note
    function saveNote() {
        const title = document.getElementById('notes-form-title').value.trim();
        const content = document.getElementById('notes-form-content').value.trim();
        const tagsInput = document.getElementById('notes-form-tags').value.trim();
        
        if (!title || !content) {
            alert('Please fill in both title and content!');
            return;
        }
        
        const tags = tagsInput 
            ? tagsInput.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)
            : [];
        
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
        
        chrome.storage.local.get(['notes'], function(result) {
            const notes = result.notes || [];
            notes.push(newNote);
            
            chrome.storage.local.set({ notes: notes }, function() {
                form.reset();
                switchTab('list');
                loadNotes();
            });
        });
    }
    
    // Escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
        // Initial load
        loadNotes();
        
        // Refresh notes every 30 seconds
        setInterval(loadNotes, 30000);
    }
    
    // Initialize widget when page is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        // DOM already loaded
        initWidget();
    }
    
})();

