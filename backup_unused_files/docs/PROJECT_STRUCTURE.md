# Clean Project Structure

## 📁 Current File Organization

```
Email_Notifications/
├── app.py                          # Main Flask application
├── document_creation.py            # Resume DOCX generation functions
├── llm_exctration.py              # LLM extraction & orchestrator
├── reaqirement_conditions.txt     # ATS optimization requirements
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
├── env_example.txt                # Environment variable template
├── run.sh                          # Application startup script
├── gui_requirements.txt           # GUI dependencies (if needed)
├── Yallaiah_Onteru.docx           # Sample resume file
└── templates/
    └── index.html                  # Web interface
```

## 🗑️ Files Removed

### Test Files (Outdated)
- `example_orchestrator_usage.py`
- `test_app.py`
- `tests/test_api.py`
- `tests/test_app.py`
- `tests/direct_test.py`

### GUI Files (Not Currently Used)
- `minimal_gui.py`
- `simple_spartex_ai.py`
- `run_gui.sh`

### Documentation (Merged/Redundant)
- `DEBUG_LOG_CLEANUP.md`
- `orchestrator_documentation.md`
- `ORCHESTRATOR_SUMMARY.md`
- `app_integration_summary.md`

### Other Unused Files
- `resume_praparation.py`
- `test_generate_resume_endpoint.py`
- `prompt.txt`
- `keywords.json`
- `scripts/setup_config.py`
- `scripts/setup.sh`

## 📋 Core Files Explained

### app.py
Main Flask application with two endpoints:
- `/process_job_description` - Email sending functionality
- `/generate_resume` - Resume generation functionality

### llm_exctration.py
Contains:
- `llm_call_skills_exctract()` - Extracts skills from job descriptions
- `llm_gold_response_call()` - Generates optimized resume JSON
- `orchestrate_resume_creation()` - Orchestrates the full pipeline
- `clean_json_response()` - Cleans LLM responses
- `load_json_prompt()` - Loads requirements from reaqirement_conditions.txt

### document_creation.py
Contains resume generation functions for 7 different styles:
- `generate_resume_style_1()` through `generate_resume_style_7()`

### reaqirement_conditions.txt
ATS optimization requirements and instructions for AI resume generation.

## 🚀 How to Use

### Start the Application
```bash
./run.sh
```

### API Endpoints

**1. Process Job Description & Send Emails**
```bash
POST http://localhost:5002/process_job_description
```

**2. Generate Resume**
```bash
POST http://localhost:5002/generate_resume
```

### Workflow

```
Job Description Input
    ↓
app.py
    ↓
orchestrate_resume_creation()
    ↓
├─ Extract Skills (LLM)
├─ Load Requirements
├─ Generate JSON
├─ Clean & Validate
└─ Generate DOCX
    ↓
Return Resume Path
```

## ✨ Clean Structure Benefits

- **Focused**: Only essential files
- **Organized**: Clear separation of concerns
- **Maintainable**: Easy to navigate and update
- **Scalable**: Ready for future features
