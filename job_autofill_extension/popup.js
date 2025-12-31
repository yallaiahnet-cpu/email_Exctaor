// Tab switching
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    loadAllData();
    setupEventListeners();
});

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            button.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
}

function setupEventListeners() {
    // Personal Info Form
    document.getElementById('personalForm').addEventListener('submit', savePersonalInfo);
    
    // Experience
    document.getElementById('addExperienceBtn').addEventListener('click', showExperienceForm);
    document.getElementById('cancelExpBtn').addEventListener('click', hideExperienceForm);
    document.getElementById('experienceFormFields').addEventListener('submit', saveExperience);
    document.getElementById('expCurrent').addEventListener('change', function() {
        document.getElementById('expEndDate').disabled = this.checked;
        if (this.checked) document.getElementById('expEndDate').value = '';
    });
    
    // Education
    document.getElementById('addEducationBtn').addEventListener('click', showEducationForm);
    document.getElementById('cancelEduBtn').addEventListener('click', hideEducationForm);
    document.getElementById('educationFormFields').addEventListener('submit', saveEducation);
    
    // Skills
    document.getElementById('saveSkillsBtn').addEventListener('click', saveSkills);
    
    // Resume
    document.getElementById('resumeFile').addEventListener('change', handleResumeUpload);
    document.getElementById('saveResumeBtn').addEventListener('click', saveResumeSettings);
    
    // Quick Actions
    document.getElementById('fillPageBtn').addEventListener('click', fillCurrentPage);
    document.getElementById('exportDataBtn').addEventListener('click', exportData);
    document.getElementById('importDataBtn').addEventListener('click', () => {
        document.getElementById('importFile').click();
    });
    document.getElementById('importFile').addEventListener('change', importData);
}

// Load all saved data
function loadAllData() {
    chrome.storage.local.get(['jobApplicationData'], function(result) {
        const data = result.jobApplicationData || {};
        loadPersonalInfo(data.personalInfo || {});
        loadExperience(data.experience || []);
        loadEducation(data.education || []);
        loadSkills(data.skills || {});
        loadResumeSettings(data.resume || {});
    });
}

// Personal Info
function loadPersonalInfo(info) {
    Object.keys(info).forEach(key => {
        const field = document.getElementById(key);
        if (field) field.value = info[key] || '';
    });
}

function savePersonalInfo(e) {
    e.preventDefault();
    const personalInfo = {
        firstName: document.getElementById('firstName').value,
        lastName: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        zipCode: document.getElementById('zipCode').value,
        country: document.getElementById('country').value,
        linkedin: document.getElementById('linkedin').value,
        github: document.getElementById('github').value,
        portfolio: document.getElementById('portfolio').value
    };
    
    chrome.storage.local.get(['jobApplicationData'], function(result) {
        const data = result.jobApplicationData || {};
        data.personalInfo = personalInfo;
        chrome.storage.local.set({ jobApplicationData: data }, function() {
            showStatus('Personal information saved!', 'success');
        });
    });
}

// Experience
function loadExperience(experience) {
    const list = document.getElementById('experienceList');
    list.innerHTML = '';
    
    if (experience.length === 0) {
        list.innerHTML = '<p style="color: #888; font-size: 13px;">No experience added yet.</p>';
        return;
    }
    
    experience.forEach((exp, index) => {
        const item = document.createElement('div');
        item.className = 'list-item';
        item.innerHTML = `
            <div class="list-item-header">
                <div>
                    <div class="list-item-title">${exp.title}</div>
                    <div class="list-item-company">${exp.company}</div>
                </div>
                <div class="list-item-date">${formatDate(exp.startDate)} - ${exp.current ? 'Present' : formatDate(exp.endDate)}</div>
            </div>
            <div class="list-item-description">${exp.description.substring(0, 150)}${exp.description.length > 150 ? '...' : ''}</div>
            <div class="list-item-actions">
                <button class="btn-small" onclick="editExperience(${index})">Edit</button>
                <button class="btn-small delete" onclick="deleteExperience(${index})">Delete</button>
            </div>
        `;
        list.appendChild(item);
    });
}

function showExperienceForm() {
    document.getElementById('experienceForm').classList.remove('hidden');
    document.getElementById('experienceFormFields').reset();
    document.getElementById('expId').value = '';
    document.getElementById('expCurrent').checked = false;
    document.getElementById('expEndDate').disabled = false;
}

function hideExperienceForm() {
    document.getElementById('experienceForm').classList.add('hidden');
}

function saveExperience(e) {
    e.preventDefault();
    const expId = document.getElementById('expId').value;
    const experience = {
        title: document.getElementById('expTitle').value,
        company: document.getElementById('expCompany').value,
        startDate: document.getElementById('expStartDate').value,
        endDate: document.getElementById('expEndDate').value,
        current: document.getElementById('expCurrent').checked,
        location: document.getElementById('expLocation').value,
        description: document.getElementById('expDescription').value
    };
    
    chrome.storage.local.get(['jobApplicationData'], function(result) {
        const data = result.jobApplicationData || {};
        if (!data.experience) data.experience = [];
        
        if (expId) {
            data.experience[parseInt(expId)] = experience;
        } else {
            data.experience.push(experience);
        }
        
        chrome.storage.local.set({ jobApplicationData: data }, function() {
            loadExperience(data.experience);
            hideExperienceForm();
            showStatus('Experience saved!', 'success');
        });
    });
}

window.editExperience = function(index) {
    chrome.storage.local.get(['jobApplicationData'], function(result) {
        const exp = result.jobApplicationData.experience[index];
        document.getElementById('expId').value = index;
        document.getElementById('expTitle').value = exp.title;
        document.getElementById('expCompany').value = exp.company;
        document.getElementById('expStartDate').value = exp.startDate;
        document.getElementById('expEndDate').value = exp.endDate || '';
        document.getElementById('expCurrent').checked = exp.current;
        document.getElementById('expEndDate').disabled = exp.current;
        document.getElementById('expLocation').value = exp.location || '';
        document.getElementById('expDescription').value = exp.description;
        document.getElementById('experienceForm').classList.remove('hidden');
    });
};

window.deleteExperience = function(index) {
    if (confirm('Delete this experience entry?')) {
        chrome.storage.local.get(['jobApplicationData'], function(result) {
            const data = result.jobApplicationData;
            data.experience.splice(index, 1);
            chrome.storage.local.set({ jobApplicationData: data }, function() {
                loadExperience(data.experience);
                showStatus('Experience deleted!', 'success');
            });
        });
    }
};

// Education
function loadEducation(education) {
    const list = document.getElementById('educationList');
    list.innerHTML = '';
    
    if (education.length === 0) {
        list.innerHTML = '<p style="color: #888; font-size: 13px;">No education added yet.</p>';
        return;
    }
    
    education.forEach((edu, index) => {
        const item = document.createElement('div');
        item.className = 'list-item';
        item.innerHTML = `
            <div class="list-item-header">
                <div>
                    <div class="list-item-title">${edu.degree}${edu.field ? ' in ' + edu.field : ''}</div>
                    <div class="list-item-company">${edu.school}</div>
                </div>
                <div class="list-item-date">${edu.endYear}</div>
            </div>
            ${edu.gpa ? `<div style="color: #666; font-size: 12px; margin-top: 5px;">GPA: ${edu.gpa}</div>` : ''}
            <div class="list-item-actions">
                <button class="btn-small" onclick="editEducation(${index})">Edit</button>
                <button class="btn-small delete" onclick="deleteEducation(${index})">Delete</button>
            </div>
        `;
        list.appendChild(item);
    });
}

function showEducationForm() {
    document.getElementById('educationForm').classList.remove('hidden');
    document.getElementById('educationFormFields').reset();
    document.getElementById('eduId').value = '';
}

function hideEducationForm() {
    document.getElementById('educationForm').classList.add('hidden');
}

function saveEducation(e) {
    e.preventDefault();
    const eduId = document.getElementById('eduId').value;
    const education = {
        school: document.getElementById('eduSchool').value,
        degree: document.getElementById('eduDegree').value,
        field: document.getElementById('eduField').value,
        startYear: document.getElementById('eduStartYear').value,
        endYear: document.getElementById('eduEndYear').value,
        gpa: document.getElementById('eduGPA').value
    };
    
    chrome.storage.local.get(['jobApplicationData'], function(result) {
        const data = result.jobApplicationData || {};
        if (!data.education) data.education = [];
        
        if (eduId) {
            data.education[parseInt(eduId)] = education;
        } else {
            data.education.push(education);
        }
        
        chrome.storage.local.set({ jobApplicationData: data }, function() {
            loadEducation(data.education);
            hideEducationForm();
            showStatus('Education saved!', 'success');
        });
    });
}

window.editEducation = function(index) {
    chrome.storage.local.get(['jobApplicationData'], function(result) {
        const edu = result.jobApplicationData.education[index];
        document.getElementById('eduId').value = index;
        document.getElementById('eduSchool').value = edu.school;
        document.getElementById('eduDegree').value = edu.degree;
        document.getElementById('eduField').value = edu.field || '';
        document.getElementById('eduStartYear').value = edu.startYear || '';
        document.getElementById('eduEndYear').value = edu.endYear;
        document.getElementById('eduGPA').value = edu.gpa || '';
        document.getElementById('educationForm').classList.remove('hidden');
    });
};

window.deleteEducation = function(index) {
    if (confirm('Delete this education entry?')) {
        chrome.storage.local.get(['jobApplicationData'], function(result) {
            const data = result.jobApplicationData;
            data.education.splice(index, 1);
            chrome.storage.local.set({ jobApplicationData: data }, function() {
                loadEducation(data.education);
                showStatus('Education deleted!', 'success');
            });
        });
    }
};

// Skills
function loadSkills(skills) {
    document.getElementById('skills').value = Array.isArray(skills.technical) ? skills.technical.join(', ') : (skills.technical || '');
    document.getElementById('certifications').value = Array.isArray(skills.certifications) ? skills.certifications.join('\n') : (skills.certifications || '');
    document.getElementById('languages').value = Array.isArray(skills.languages) ? skills.languages.join(', ') : (skills.languages || '');
}

function saveSkills() {
    const skills = {
        technical: document.getElementById('skills').value.split(',').map(s => s.trim()).filter(s => s),
        certifications: document.getElementById('certifications').value.split('\n').map(s => s.trim()).filter(s => s),
        languages: document.getElementById('languages').value.split(',').map(s => s.trim()).filter(s => s)
    };
    
    chrome.storage.local.get(['jobApplicationData'], function(result) {
        const data = result.jobApplicationData || {};
        data.skills = skills;
        chrome.storage.local.set({ jobApplicationData: data }, function() {
            showStatus('Skills saved!', 'success');
        });
    });
}

// Resume
function loadResumeSettings(resume) {
    document.getElementById('coverLetter').value = resume.coverLetter || '';
    if (resume.fileName) {
        document.getElementById('resumeStatus').innerHTML = `
            <div class="status-message success">
                Resume file: ${resume.fileName}
            </div>
        `;
    }
}

function handleResumeUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    if (file.size > 5 * 1024 * 1024) {
        showStatus('File too large! Maximum 5MB.', 'error');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(event) {
        const base64 = event.target.result;
        chrome.storage.local.get(['jobApplicationData'], function(result) {
            const data = result.jobApplicationData || {};
            if (!data.resume) data.resume = {};
            data.resume.fileData = base64;
            data.resume.fileName = file.name;
            data.resume.fileType = file.type;
            chrome.storage.local.set({ jobApplicationData: data }, function() {
                loadResumeSettings(data.resume);
                showStatus('Resume uploaded!', 'success');
            });
        });
    };
    reader.readAsDataURL(file);
}

function saveResumeSettings() {
    chrome.storage.local.get(['jobApplicationData'], function(result) {
        const data = result.jobApplicationData || {};
        if (!data.resume) data.resume = {};
        data.resume.coverLetter = document.getElementById('coverLetter').value;
        chrome.storage.local.set({ jobApplicationData: data }, function() {
            showStatus('Resume settings saved!', 'success');
        });
    });
}

// Quick Actions
function fillCurrentPage() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'fillForm' }, function(response) {
            if (chrome.runtime.lastError) {
                showStatus('Error: ' + chrome.runtime.lastError.message, 'error');
            } else if (response && response.success) {
                showStatus('Form filled successfully!', 'success');
            } else {
                showStatus('No form fields detected on this page.', 'info');
            }
        });
    });
}

function exportData() {
    chrome.storage.local.get(['jobApplicationData'], function(result) {
        const data = result.jobApplicationData || {};
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'job-application-data.json';
        a.click();
        URL.revokeObjectURL(url);
        showStatus('Data exported!', 'success');
    });
}

function importData(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(event) {
        try {
            const data = JSON.parse(event.target.result);
            chrome.storage.local.set({ jobApplicationData: data }, function() {
                loadAllData();
                showStatus('Data imported successfully!', 'success');
            });
        } catch (error) {
            showStatus('Invalid JSON file!', 'error');
        }
    };
    reader.readAsText(file);
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString + '-01');
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
}

function showStatus(message, type) {
    const statusDiv = document.getElementById('statusMessage');
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;
    setTimeout(() => {
        statusDiv.textContent = '';
        statusDiv.className = 'status-message';
    }, 3000);
}



