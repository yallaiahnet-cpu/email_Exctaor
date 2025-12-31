# Resume Creation Summary

## ✅ What Was Created

1. **`create_resume.py`** - Simple script to create resumes by calling ResumeOptimizer
2. **`tests/test_resume_optimizer.py`** - Test suite for ResumeOptimizer class
3. **`CREATE_RESUME_USAGE.md`** - Documentation on how to use the class

## 🚀 Quick Start

### Create a Resume (Simple Way)

```bash
python create_resume.py
```

### Create a Resume (With Custom JD)

```bash
python create_resume.py "Your job description here"
```

### Create a Resume (Python Code)

```python
from llm_exctration import ResumeOptimizer

# Pass your job description
jd = "Your job description here..."
optimizer = ResumeOptimizer(jd)

# Call workflow() to create resume
resume_path = optimizer.workflow()
print(f"Resume saved at: {resume_path}")
```

## 📁 Where Resumes are Saved

Resumes are saved in: `resumes/optimized_resume_YYYYMMDD_HHMMSS.json`

Example: `resumes/optimized_resume_20251026_044512.json`

## ⚙️ How It Works in Your App

When user clicks "Create Resume" button in the frontend:

```
Frontend (index.html)
    ↓ sends job description
    ↓
Flask App (app.py)
    ↓ creates ResumeOptimizer(jd)
    ↓ calls optimizer.workflow()
    ↓
ResumeOptimizer (llm_exctration.py)
    ├─ Step 1: extract_skills()
    ├─ Step 2: generate_resume()
    └─ Step 3: create_document()
    ↓
returns file path
    ↓
Frontend displays success message
```

## 📝 Code in app.py

The integration in `app.py` (lines 438-459):

```python
from llm_exctration import ResumeOptimizer

# Create instance with job description
optimizer = ResumeOptimizer(job_description)

# Execute complete workflow
resume_path = optimizer.workflow()

# Return success response
return jsonify({
    'message': 'Resume generated successfully',
    'resume_path': resume_path,
    'timestamp': timestamp
})
```

## ⚠️ Current Issue

The ResumeOptimizer class has a very large system prompt that exceeds Groq's token limit (6000 TPM for free tier). The system needs:

1. **Shorter system prompt** - Reduce the SYSTEM_PROMPT size
2. **Or use a larger model** - Upgrade Groq plan
3. **Or chunk the prompt** - Break it into smaller parts

## 🧪 Running Tests

```bash
# Run all tests
python tests/test_resume_optimizer.py

# Or use pytest
pytest tests/

# Or use unittest
python -m unittest tests.test_resume_optimizer
```

## 📊 Test Results

- ✅ Initialization: Working
- ✅ Skill Extraction: Working
- ⚠️ Resume Generation: Token limit issues
- ✅ Document Creation: Working
- ✅ Complete Workflow: Working
- ✅ Different JDs: Working

## 🎯 Next Steps

1. **Reduce system prompt size** in `llm_exctration.py` (SYSTEM_PROMPT variable)
2. **Test with shorter prompts** to avoid token limits
3. **Consider upgrading Groq plan** for higher limits

Google CCAI Developer (Dialogflow & Node.js)
Any | ITTConnect | United States

Posted On 09-Oct-2025
Job Description
ITTConnect is seeking a Google Cloud Contact Center Developer - (Dialogflow & Node.js) to work for one of our clients. This is a role with a global leader in consulting, digital transformation, technology and engineering services present in nearly 50 countries. The end client is in the Telecom business. 


Job location: Hybrid in Atlanta, zip code 30328 (3 days per week in the office).

Key responsibilities:
Conversational Design & UX: Design conversational flows using Dialogflow CX, incorporating best practices for dialogue flow, branching logic, error handling, and persona development.
GCP & Agent Assist Integration: Integrate Dialogflow CX with Agent Assist to provide real-time guidance and knowledge access to contact center agents. 
Plan for custom integrations using APIs and scripting languages (e.g., Python, JavaScript, Node.js).
Debug and troubleshoot issues in conversational flows and integrations.
Analyze data from Dialogflow CX to identify areas for improvement and measure success.
Collaboration & Communication: Collaborate with cross-functional teams (including designers, engineers, and client stakeholders) to deliver high-quality conversational AI solutions. Effectively communicate technical concepts to both technical and non-technical audiences.


Requirements

8+ years of experience in Application Development and at least 3+ years in the Contact Center space
Minimum of 2 years of experience in Node.js, as well as Git, Jira, etc.
Good knowledge of Google Cloud Platform CCAI service, Dialog flow CX, and Agent Assist.
Proficiency in using dialogue flow design tools like Dialogflow CX, including fulfillment, integrations, webhooks, and analytics.
Solid understanding of GCP fundamentals (Compute Engine, Cloud Storage, Cloud Functions, APIs).
Knowledge of GCP and GDF architecture
Playbooks and GCP cloud run
Experience in Telco domain and processes.
Experience with API integration (REST, gRPC) and Cloud Functions, as well as CI/CD pipelines.
Should be able to follow Agile Scrum cadence.


 
