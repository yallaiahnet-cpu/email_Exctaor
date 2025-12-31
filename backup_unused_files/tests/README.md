# Tests for Email Notifications Project

This directory contains test files for the Email Notifications project.

## Test Files

- `test_resume_optimizer.py` - Tests for the ResumeOptimizer class

## Running Tests

### Run all tests
```bash
python -m pytest tests/
```

### Run specific test file
```bash
python -m pytest tests/test_resume_optimizer.py
```

### Run with verbose output
```bash
python -m pytest tests/ -v
```

### Run the test file directly
```bash
python tests/test_resume_optimizer.py
```

## Test Coverage

The test suite covers:
- ResumeOptimizer initialization
- Skill extraction from job descriptions
- Resume JSON generation
- Document creation
- Complete workflow execution
- Different job descriptions handling

## Requirements

Make sure you have:
- Python 3.9+
- Required packages from requirements.txt
- GROQ_API_KEY environment variable set
- `.env` file configured

