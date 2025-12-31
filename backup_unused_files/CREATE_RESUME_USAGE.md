# How to Create a Resume Using ResumeOptimizer

## Method 1: Using the create_resume.py Script

### Run with default job description:
```bash
python create_resume.py
```

### Run with custom job description:
```bash
python create_resume.py "Your job description text here"
```

## Method 2: Using in Python Code

```python
from llm_exctration import ResumeOptimizer

# Your job description
job_description = """
Position: Data Engineer AI/ML Pipelines
Location: Seffner FL (Hybrid)

Requirements:
- Develop backend services and APIs for WMS
- Build ETL/ELT pipelines using Azure Data Factory & Databricks
- Implement CI/CD, instrumentation, and observability
- Python, C#/.NET, Java for app development
- Advanced SQL and distributed data systems
- 5+ years in software development/data engineering
"""

# Create optimizer instance
optimizer = ResumeOptimizer(job_description)

# Execute complete workflow
resume_path = optimizer.workflow()

print(f"Resume saved at: {resume_path}")
```

## Method 3: Step-by-Step (More Control)

```python
from llm_exctration import ResumeOptimizer

# Create optimizer
optimizer = ResumeOptimizer(job_description)

# Step 1: Extract skills
print("Extracting skills...")
optimizer.extract_skills()
print(f"Skills extracted: {optimizer.extracted_skills[:100]}...")

# Step 2: Generate resume JSON
print("\nGenerating resume...")
resume_json = optimizer.generate_resume()
print(f"Resume generated with {len(resume_json)} fields")

# Step 3: Create document
print("\nCreating document...")
file_path = optimizer.create_document()
print(f"Document created at: {file_path}")
```

## Method 4: Using from Flask App (app.py)

The `app.py` already integrates the ResumeOptimizer. When you click "Create Resume" button in the web interface:

1. Frontend sends job description to `/generate_resume` endpoint
2. Backend creates `ResumeOptimizer(job_description)`
3. Calls `optimizer.workflow()`
4. Returns the resume file path to the frontend

## Output

Resumes are saved in the `resumes/` directory with timestamped filenames:
```
resumes/optimized_resume_20251026_044336.json
```

## Requirements

- Python 3.9+
- .env file with `GROQ_API_KEY`
- All dependencies installed from requirements.txt

## Troubleshooting

If you get "Request too large" errors:
- The system prompt is too long for the current model
- Consider reducing the system prompt size in `llm_exctration.py`
- Or upgrade to a larger Groq model

