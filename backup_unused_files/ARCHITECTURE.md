# System Architecture

## Resume Creation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│                   (templates/index.html)                      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Job Desc     │  │ Create       │  │ Preview      │      │
│  │ Input        │→ │ Resume Btn   │→ │ & Send       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                   FLASK BACKEND                              │
│                    (app.py)                                 │
│                                                               │
│  @app.route('/generate_resume')                             │
│    ↓                                                         │
│  ResumeOptimizer(job_description)                           │
│    ↓                                                         │
│  optimizer.workflow()                                        │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────┐
│              RESUME OPTIMIZER CLASS                          │
│              (llm_exctration.py)                             │
│                                                               │
│  ┌─────────────────────────────────────────┐                │
│  │ Step 1: extract_skills()                │                │
│  │  - Analyze JD with LLM                   │                │
│  │  - Extract technical skills             │                │
│  │  - Store in self.extracted_skills        │                │
│  └─────────────────────────────────────────┘                │
│                               ↓                             │
│  ┌─────────────────────────────────────────┐                │
│  │ Step 2: generate_resume()                │                │
│  │  - Use extracted skills + JD             │                │
│  │  - Call LLM to generate resume JSON      │                │
│  │  - Store in self.resume_json             │                │
│  └─────────────────────────────────────────┘                │
│                               ↓                             │
│  ┌─────────────────────────────────────────┐                │
│  │ Step 3: create_document()               │                │
│  │  - Save JSON to file                    │                │
│  │  - Return file path                     │                │
│  └─────────────────────────────────────────┘                │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ↓
                    ┌─────────────────┐
                    │  resumes/       │
                    │  optimized_    │
                    │  resume_       │
                    │  YYYYMMDD_     │
                    │  HHMMSS.json   │
                    └─────────────────┘
```

## API Endpoints

### `/generate_resume` (POST)

**Request:**
```json
{
  "job_description": "JD text here..."
}
```

**Response (Success):**
```json
{
  "message": "Resume generated successfully",
  "resume_path": "resumes/optimized_resume_20251026_044512.json",
  "timestamp": "20251026_044512"
}
```

**Response (Error):**
```json
{
  "error": "Failed to generate resume"
}
```

## File Structure

```
Email_Notifications/
├── app.py                  # Flask backend
├── llm_exctration.py       # ResumeOptimizer class
├── create_resume.py        # Standalone script
├── tests/
│   ├── __init__.py
│   ├── test_resume_optimizer.py
│   └── README.md
├── templates/
│   └── index.html          # Frontend UI
├── resumes/                # Output directory
│   └── optimized_resume_*.json
└── *.md                    # Documentation

```

## Class Methods

### ResumeOptimizer

```python
class ResumeOptimizer:
    def __init__(self, job_description: str)
        """Initialize with job description"""
    
    def extract_skills(self) -> str
        """Extract skills from JD using LLM"""
    
    def generate_resume(self) -> dict
        """Generate resume JSON"""
    
    def create_document(self) -> str
        """Save JSON to file, return path"""
    
    def workflow(self) -> str
        """Complete workflow: extract → generate → create"""
```

## Call Chain

```
User clicks "Create Resume"
    ↓
index.html → fetch('/generate_resume', {...})
    ↓
app.py → ResumeOptimizer(jd)
    ↓
llm_exctration.py → optimizer.workflow()
    ↓
    ├─ extract_skills() → LLM API
    ├─ generate_resume() → LLM API  
    └─ create_document() → File system
    ↓
Response → resume_path
    ↓
Frontend displays path

