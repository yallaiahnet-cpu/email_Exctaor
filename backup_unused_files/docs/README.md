# Email Notifications API

A Flask-based API that automatically extracts job details from job descriptions using AI and sends personalized emails with resume attachments.

## Features

- 🤖 **AI-Powered Extraction**: Uses Groq API to extract emails, skills, job titles, company names, and recruiter information
- 📧 **SMTP Email Sending**: Sends professional emails with PDF resume attachments
- 🌐 **Web Interface**: HTML frontend for easy interaction
- 📄 **Resume Attachment**: Automatically attaches PDF resume to emails
- 🎯 **Smart Parsing**: Extracts recruiter names and personalizes email greetings
- 📝 **AI Resume Generation**: Generate ATS-optimized resumes from job descriptions
- 🔄 **Orchestrator Pattern**: End-to-end resume creation pipeline

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp env_example.txt .env
# Edit .env with your SMTP and Groq API credentials
```

### 3. Run the Application

**Web Interface:**
```bash
python3 app.py
```
The API will be available at `http://localhost:5002`

**Beautiful GUI Interface:**
```bash
./run_gui.sh
# or
python3 frosted_glass_ai.py
```

## Configuration

Create a `.env` file with the following variables:

```env
# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key

# Resume File Path
PDF_RESUME_PATH=/path/to/your/resume.pdf

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

## API Endpoints

### POST `/process_job_description`
Process a job description and send emails.

**Request Body:**
```json
{
  "job_description": "Job description text...",
  "use_groq": true,
  "attach_pdf": true
}
```

**Response:**
```json
{
  "message": "Processing completed",
  "extracted_emails": ["email@example.com"],
  "extracted_skills": ["Python", "AI/ML"],
  "job_title": "Software Engineer",
  "recruiter_name": "John Doe",
  "email_subject": "Application for Software Engineer – Remote",
  "total_emails_sent": 1,
  "email_results": [{"email": "email@example.com", "sent": true, "status": "success"}]
}
```

### GET `/health`
Check API health status.

## Web Interface

Access the web interface at `http://localhost:5002` to:
- Paste job descriptions
- Preview extracted information
- Send emails with resume attachments

## Project Structure

```
Email_Notifications/
├── app.py                 # Main Flask application
├── frosted_glass_ai.py    # Beautiful GUI application
├── templates/
│   └── index.html         # Web interface
├── tests/                 # Test files
├── scripts/               # Setup and utility scripts
├── requirements.txt       # Flask API dependencies
├── gui_requirements.txt   # GUI dependencies
├── run.sh                 # Run Flask API
├── run_gui.sh             # Run GUI application
└── env_example.txt       # Environment variables template
```

## Testing

Run tests from the `tests/` directory:
```bash
cd tests
python3 test_api.py
```

## Setup Scripts

Use the setup scripts in the `scripts/` directory:
```bash
cd scripts
./setup.sh
```

## License

This project is for personal use. Please ensure you comply with email service terms and conditions.