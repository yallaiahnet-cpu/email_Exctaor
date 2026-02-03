// Field mapping patterns for common job sites
const FIELD_PATTERNS = {
    firstName: [
        'firstname', 'first-name', 'first_name', 'fname', 'given-name', 'given_name',
        'firstName', 'FirstName', 'first', 'name[first]', 'applicant[first_name]'
    ],
    lastName: [
        'lastname', 'last-name', 'last_name', 'lname', 'family-name', 'family_name',
        'lastName', 'LastName', 'last', 'surname', 'name[last]', 'applicant[last_name]'
    ],
    email: [
        'email', 'email-address', 'email_address', 'e-mail', 'e_mail',
        'Email', 'EMAIL', 'applicant[email]', 'user[email]'
    ],
    phone: [
        'phone', 'phone-number', 'phone_number', 'telephone', 'tel', 'mobile',
        'Phone', 'phoneNumber', 'applicant[phone]', 'contact[phone]'
    ],
    address: [
        'address', 'street-address', 'street_address', 'street', 'address-line-1',
        'addressLine1', 'applicant[address]'
    ],
    city: [
        'city', 'City', 'applicant[city]', 'location[city]'
    ],
    state: [
        'state', 'State', 'province', 'applicant[state]', 'location[state]'
    ],
    zipCode: [
        'zip', 'zipcode', 'zip-code', 'zip_code', 'postal-code', 'postal_code',
        'postal', 'ZipCode', 'applicant[zip]', 'location[zip]'
    ],
    country: [
        'country', 'Country', 'applicant[country]', 'location[country]'
    ],
    linkedin: [
        'linkedin', 'linked-in', 'linked_in', 'linkedin-url', 'linkedin_url',
        'LinkedIn', 'linkedinProfile', 'applicant[linkedin]'
    ],
    github: [
        'github', 'github-url', 'github_url', 'GitHub', 'githubProfile',
        'applicant[github]'
    ],
    portfolio: [
        'portfolio', 'website', 'portfolio-url', 'portfolio_url', 'personal-website',
        'applicant[portfolio]', 'applicant[website]'
    ]
};

// Experience field patterns
const EXPERIENCE_PATTERNS = {
    title: ['job-title', 'job_title', 'position', 'role', 'title', 'JobTitle'],
    company: ['company', 'employer', 'organization', 'organization-name', 'company-name'],
    startDate: ['start-date', 'start_date', 'startDate', 'employment-start', 'from-date'],
    endDate: ['end-date', 'end_date', 'endDate', 'employment-end', 'to-date', 'current'],
    location: ['location', 'job-location', 'work-location', 'city'],
    description: ['description', 'responsibilities', 'duties', 'summary', 'details']
};

// Education field patterns
const EDUCATION_PATTERNS = {
    school: ['school', 'university', 'college', 'institution', 'school-name'],
    degree: ['degree', 'qualification', 'education-level', 'degree-type'],
    field: ['field', 'major', 'subject', 'field-of-study', 'specialization'],
    startYear: ['start-year', 'startYear', 'from-year', 'education-start'],
    endYear: ['end-year', 'endYear', 'graduation-year', 'to-year', 'graduation'],
    gpa: ['gpa', 'GPA', 'grade-point-average', 'grade']
};

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

function init() {
    // Listen for messages from popup
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'fillForm') {
            fillForm().then(result => {
                sendResponse(result);
            }).catch(error => {
                sendResponse({ success: false, error: error.message });
            });
            return true; // Keep channel open for async response
        }
    });

    // Add visual indicator button
    addFillButton();
}

// Add floating fill button
function addFillButton() {
    // Check if button already exists
    if (document.getElementById('job-autofill-btn')) return;

    const button = document.createElement('div');
    button.id = 'job-autofill-btn';
    button.innerHTML = '🚀 Fill Form';
    button.title = 'Click to auto-fill this form';
    button.addEventListener('click', () => {
        fillForm().then(result => {
            if (result.success) {
                showNotification('Form filled successfully!', 'success');
            } else {
                showNotification(result.message || 'No form fields found', 'info');
            }
        });
    });
    document.body.appendChild(button);
}

// Main fill function
async function fillForm() {
    try {
        const data = await getStoredData();
        if (!data || !data.personalInfo) {
            return { success: false, message: 'No data found. Please add your information in the extension popup.' };
        }

        let filledCount = 0;
        
        // Fill personal information
        filledCount += fillPersonalInfo(data.personalInfo);
        
        // Fill experience if forms are present
        if (data.experience && data.experience.length > 0) {
            filledCount += fillExperience(data.experience);
        }
        
        // Fill education if forms are present
        if (data.education && data.education.length > 0) {
            filledCount += fillEducation(data.education);
        }
        
        // Fill skills
        if (data.skills) {
            filledCount += fillSkills(data.skills);
        }
        
        // Fill cover letter
        if (data.resume && data.resume.coverLetter) {
            filledCount += fillCoverLetter(data.resume.coverLetter);
        }

        // Handle file uploads
        if (data.resume && data.resume.fileData) {
            await handleResumeUpload(data.resume);
        }

        return {
            success: filledCount > 0,
            message: `Filled ${filledCount} field(s)`,
            count: filledCount
        };
    } catch (error) {
        console.error('Error filling form:', error);
        return { success: false, message: error.message };
    }
}

// Get stored data
function getStoredData() {
    return new Promise((resolve) => {
        chrome.storage.local.get(['jobApplicationData'], (result) => {
            resolve(result.jobApplicationData);
        });
    });
}

// Fill personal information
function fillPersonalInfo(info) {
    let filled = 0;
    
    Object.keys(FIELD_PATTERNS).forEach(key => {
        if (!info[key]) return;
        
        const value = info[key];
        const patterns = FIELD_PATTERNS[key];
        
        patterns.forEach(pattern => {
            // Try by name
            let field = findFieldByName(pattern);
            if (!field) {
                // Try by id
                field = document.getElementById(pattern);
            }
            if (!field) {
                // Try by placeholder
                field = findFieldByPlaceholder(key, pattern);
            }
            if (!field) {
                // Try by label
                field = findFieldByLabel(key);
            }
            
            if (field && !field.value) {
                fillField(field, value);
                filled++;
            }
        });
    });
    
    return filled;
}

// Fill experience
function fillExperience(experience) {
    let filled = 0;
    
    // Find all experience forms (could be multiple entries)
    const experienceSections = findExperienceSections();
    
    experience.forEach((exp, index) => {
        if (index >= experienceSections.length) return;
        
        const section = experienceSections[index];
        const fields = {
            title: findFieldInSection(section, EXPERIENCE_PATTERNS.title),
            company: findFieldInSection(section, EXPERIENCE_PATTERNS.company),
            startDate: findFieldInSection(section, EXPERIENCE_PATTERNS.startDate),
            endDate: findFieldInSection(section, EXPERIENCE_PATTERNS.endDate),
            location: findFieldInSection(section, EXPERIENCE_PATTERNS.location),
            description: findFieldInSection(section, EXPERIENCE_PATTERNS.description)
        };
        
        if (fields.title && exp.title) {
            fillField(fields.title, exp.title);
            filled++;
        }
        if (fields.company && exp.company) {
            fillField(fields.company, exp.company);
            filled++;
        }
        if (fields.startDate && exp.startDate) {
            fillField(fields.startDate, formatDateForInput(exp.startDate));
            filled++;
        }
        if (fields.endDate && !exp.current && exp.endDate) {
            fillField(fields.endDate, formatDateForInput(exp.endDate));
            filled++;
        }
        if (fields.location && exp.location) {
            fillField(fields.location, exp.location);
            filled++;
        }
        if (fields.description && exp.description) {
            fillField(fields.description, exp.description);
            filled++;
        }
    });
    
    return filled;
}

// Fill education
function fillEducation(education) {
    let filled = 0;
    
    const educationSections = findEducationSections();
    
    education.forEach((edu, index) => {
        if (index >= educationSections.length) return;
        
        const section = educationSections[index];
        const fields = {
            school: findFieldInSection(section, EDUCATION_PATTERNS.school),
            degree: findFieldInSection(section, EDUCATION_PATTERNS.degree),
            field: findFieldInSection(section, EDUCATION_PATTERNS.field),
            endYear: findFieldInSection(section, EDUCATION_PATTERNS.endYear),
            gpa: findFieldInSection(section, EDUCATION_PATTERNS.gpa)
        };
        
        if (fields.school && edu.school) {
            fillField(fields.school, edu.school);
            filled++;
        }
        if (fields.degree && edu.degree) {
            fillField(fields.degree, edu.degree);
            filled++;
        }
        if (fields.field && edu.field) {
            fillField(fields.field, edu.field);
            filled++;
        }
        if (fields.endYear && edu.endYear) {
            fillField(fields.endYear, edu.endYear);
            filled++;
        }
        if (fields.gpa && edu.gpa) {
            fillField(fields.gpa, edu.gpa);
            filled++;
        }
    });
    
    return filled;
}

// Fill skills
function fillSkills(skills) {
    let filled = 0;
    
    // Technical skills
    if (skills.technical && skills.technical.length > 0) {
        const skillsText = skills.technical.join(', ');
        const skillsField = findFieldByName('skills') || 
                          findFieldByPlaceholder('skills', 'technical') ||
                          document.querySelector('textarea[name*="skill"], input[name*="skill"]');
        if (skillsField) {
            fillField(skillsField, skillsText);
            filled++;
        }
    }
    
    // Certifications
    if (skills.certifications && skills.certifications.length > 0) {
        const certsText = skills.certifications.join('\n');
        const certsField = findFieldByName('certification') ||
                          findFieldByPlaceholder('certification', 'cert');
        if (certsField) {
            fillField(certsField, certsText);
            filled++;
        }
    }
    
    return filled;
}

// Fill cover letter
function fillCoverLetter(coverLetter) {
    const coverLetterField = findFieldByName('cover-letter') ||
                            findFieldByName('coverletter') ||
                            findFieldByPlaceholder('cover', 'letter') ||
                            document.querySelector('textarea[name*="cover"], textarea[id*="cover"]');
    if (coverLetterField && !coverLetterField.value) {
        fillField(coverLetterField, coverLetter);
        return 1;
    }
    return 0;
}

// Handle resume file upload
async function handleResumeUpload(resumeData) {
    const fileInput = document.querySelector('input[type="file"][accept*="pdf"], input[type="file"][accept*="doc"], input[type="file"][name*="resume"], input[type="file"][name*="cv"]');
    
    if (!fileInput) return;
    
    try {
        // Convert base64 to blob
        const response = await fetch(resumeData.fileData);
        const blob = await response.blob();
        const file = new File([blob], resumeData.fileName, { type: resumeData.fileType });
        
        // Create a DataTransfer object to set files
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        
        // Trigger change event
        const event = new Event('change', { bubbles: true });
        fileInput.dispatchEvent(event);
        
        return 1;
    } catch (error) {
        console.error('Error uploading resume:', error);
        return 0;
    }
}

// Helper functions
function findFieldByName(pattern) {
    const selectors = [
        `input[name="${pattern}"]`,
        `input[name*="${pattern}"]`,
        `textarea[name="${pattern}"]`,
        `textarea[name*="${pattern}"]`,
        `select[name="${pattern}"]`,
        `select[name*="${pattern}"]`
    ];
    
    for (const selector of selectors) {
        const field = document.querySelector(selector);
        if (field && (field.type !== 'hidden' && field.type !== 'submit' && field.type !== 'button')) {
            return field;
        }
    }
    return null;
}

function findFieldByPlaceholder(key, pattern) {
    const fields = document.querySelectorAll('input, textarea, select');
    for (const field of fields) {
        const placeholder = (field.placeholder || '').toLowerCase();
        const name = (field.name || '').toLowerCase();
        const id = (field.id || '').toLowerCase();
        
        if (placeholder.includes(key.toLowerCase()) || 
            placeholder.includes(pattern.toLowerCase()) ||
            name.includes(key.toLowerCase()) ||
            id.includes(key.toLowerCase())) {
            if (field.type !== 'hidden' && field.type !== 'submit' && field.type !== 'button') {
                return field;
            }
        }
    }
    return null;
}

function findFieldByLabel(key) {
    const labels = document.querySelectorAll('label');
    for (const label of labels) {
        const text = label.textContent.toLowerCase();
        if (text.includes(key.toLowerCase())) {
            const forAttr = label.getAttribute('for');
            if (forAttr) {
                const field = document.getElementById(forAttr);
                if (field) return field;
            }
            // Try to find input inside label
            const field = label.querySelector('input, textarea, select');
            if (field) return field;
        }
    }
    return null;
}

function findFieldInSection(section, patterns) {
    for (const pattern of patterns) {
        const field = section.querySelector(`input[name*="${pattern}"], textarea[name*="${pattern}"], select[name*="${pattern}"]`) ||
                     section.querySelector(`input[id*="${pattern}"], textarea[id*="${pattern}"], select[id*="${pattern}"]`);
        if (field) return field;
    }
    return null;
}

function findExperienceSections() {
    // Common patterns for experience sections
    const selectors = [
        '[class*="experience"]',
        '[class*="employment"]',
        '[class*="work-history"]',
        '[id*="experience"]',
        '[id*="employment"]',
        'fieldset:has(input[name*="job"], input[name*="company"])'
    ];
    
    const sections = [];
    selectors.forEach(selector => {
        try {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                if (el.querySelector('input[name*="title"], input[name*="company"]')) {
                    sections.push(el);
                }
            });
        } catch (e) {
            // Invalid selector, skip
        }
    });
    
    return sections.length > 0 ? sections : [document.body]; // Fallback to body
}

function findEducationSections() {
    const selectors = [
        '[class*="education"]',
        '[class*="school"]',
        '[id*="education"]',
        'fieldset:has(input[name*="school"], input[name*="degree"])'
    ];
    
    const sections = [];
    selectors.forEach(selector => {
        try {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                if (el.querySelector('input[name*="school"], input[name*="degree"]')) {
                    sections.push(el);
                }
            });
        } catch (e) {
            // Invalid selector, skip
        }
    });
    
    return sections.length > 0 ? sections : [document.body];
}

function fillField(field, value) {
    if (!field || !value) return;
    
    // Set value
    field.value = value;
    
    // Trigger events
    field.dispatchEvent(new Event('input', { bubbles: true }));
    field.dispatchEvent(new Event('change', { bubbles: true }));
    
    // For React and other frameworks
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    if (nativeInputValueSetter) {
        nativeInputValueSetter.call(field, value);
        field.dispatchEvent(new Event('input', { bubbles: true }));
    }
}

function formatDateForInput(dateString) {
    if (!dateString) return '';
    // If it's already in YYYY-MM format, return as is
    if (/^\d{4}-\d{2}$/.test(dateString)) {
        return dateString;
    }
    // Try to parse and format
    const date = new Date(dateString);
    if (!isNaN(date.getTime())) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        return `${year}-${month}`;
    }
    return dateString;
}

function showNotification(message, type) {
    // Remove existing notification
    const existing = document.getElementById('job-autofill-notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.id = 'job-autofill-notification';
    notification.textContent = message;
    notification.className = `job-autofill-notification ${type}`;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}



