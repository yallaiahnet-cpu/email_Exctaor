from flask import Flask, request, jsonify, render_template, send_file
import json
import re
import os
from datetime import datetime
from dotenv import load_dotenv
from cleaning_jd import EmailExtractor
from send_email import EmailSender
from llm_exctration import ResumeOptimizer
from document_creation import generate_resume_style_1

# Load environment variables
load_dotenv()

app2 = Flask(__name__)

# Initialize EmailSender for second email account
SMTP_USERNAME_2 = os.getenv('SMTP_USERNAME_2', '')
SMTP_PASSWORD_2 = os.getenv('SMTP_PASSWORD_2', '')
RESUME_FILE_2 = os.getenv('PDF_RESUME_PATH_2', '')

email_sender_2 = EmailSender(
    sender_email=SMTP_USERNAME_2,
    app_password=SMTP_PASSWORD_2,
    resume_file=RESUME_FILE_2
)

@app2.route('/')
def index():
    return render_template('index.html')

@app2.route('/clean_job_description', methods=['POST'])
def clean_job_description():
    try:
        # Get input from frontend
        print("=== Receiving input from frontend ===")
        raw_text = request.get_json()['raw_text']
        print(f"Input length: {len(raw_text)} chars")
        
        # Pass to cleaning_jd.py (port 5003 uses profile 2)
        print("\n=== Calling cleaning_jd.py EmailExtractor ===")
        extractor = EmailExtractor(raw_text, use_profile_2=True)
        print("Extractor created")
        
        result_json = extractor.extract_email_info_from_jd(raw_text)
        print(f"\n=== Response from cleaning_jd.py ===\nLength: {len(result_json)} chars\nFirst 200 chars: {result_json[:200]}")
        
        # Try to parse JSON directly first
        try:
            result_dict = json.loads(result_json)
            print("\n=== Successfully parsed JSON on first try ===")
            return jsonify(result_dict), 200
        except json.JSONDecodeError:
            print("\n=== First parse failed, trying to fix newlines ===")
            # Extract JSON and try to fix it
            json_match = re.search(r'\{.*\}', result_json, re.DOTALL)
            if json_match:
                cleaned_json = json_match.group(0)
                # Try multiple parsing strategies
                for strategy in ['direct', 'replace_all']:
                    try:
                        if strategy == 'direct':
                            result_dict = json.loads(cleaned_json)
                            print("=== Parsed successfully with direct method ===")
                        elif strategy == 'replace_all':
                            fixed_json = cleaned_json.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                            result_dict = json.loads(fixed_json)
                            print("=== Parsed successfully by replacing all newlines with spaces ===")
                        return jsonify(result_dict), 200
                    except json.JSONDecodeError:
                        continue
            print("\n❌ No valid JSON found after all attempts")
            return jsonify({'error': 'No valid JSON found in response'}), 500
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON Error: {str(e)}")
        return jsonify({'error': f'Failed to parse JSON: {str(e)}'}), 500
    except Exception as e:
        print(f"\n❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app2.route('/list_resumes', methods=['GET'])
def list_resumes():
    """List available resume files"""
    try:
        resumes = []
        
        # Check root directory
        root_dir = os.getcwd()
        for file in os.listdir(root_dir):
            if file.endswith(('.pdf', '.docx', '.doc')):
                full_path = os.path.join(root_dir, file)
                if os.path.isfile(full_path):
                    resumes.append(full_path)
        
        # Check generated_resumes directory
        resume_directory = os.path.join(root_dir, 'generated_resumes')
        if os.path.exists(resume_directory):
            for root, dirs, files in os.walk(resume_directory):
                for file in files:
                    if file.endswith(('.pdf', '.docx', '.doc')):
                        full_path = os.path.join(root, file)
                        if full_path not in resumes:
                            resumes.append(full_path)
        
        resumes.sort()
        return jsonify({'resumes': resumes}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app2.route('/create_resume', methods=['POST'])
def create_resume():
    """Create optimized resume using ResumeOptimizer and convert to DOCX"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        print(f"\n=== Creating Resume ===")
        print(f"Job description length: {len(job_description)} chars")
        
        # Step 1: Initialize ResumeOptimizer
        optimizer = ResumeOptimizer(job_description)
        
        # Step 2: Extract skills from job description
        print("\n=== Step 1: Extracting skills from JD ===")
        extracted_skills = optimizer.extract_skills()
        print(f"✅ Skills extracted: {len(extracted_skills)} chars")
        
        # Step 3: Generate optimized resume JSON
        print("\n=== Step 2: Generating optimized resume ===")
        optimizer.generate_resume()
        
        if not optimizer.resume_json:
            return jsonify({'error': 'Failed to generate resume JSON'}), 500
        
        # Validate and ensure JSON is a dict, not a string
        print("\n=== Step 3: Validating JSON ===")
        if isinstance(optimizer.resume_json, str):
            optimizer.resume_json = json.loads(optimizer.resume_json)
        
        json.dumps(optimizer.resume_json)  # This will raise error if invalid
        print("✅ JSON is valid")
        
        # Step 4: Save JSON file
        print("\n=== Step 4: Saving JSON file ===")
        output_dir = "resumes"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"optimized_resume_{timestamp}.json"
        json_resume_path = os.path.join(output_dir, json_filename)
        
        with open(json_resume_path, 'w') as f:
            json.dump(optimizer.resume_json, f, indent=2)
        print(f"✅ JSON saved at: {json_resume_path}")
        
        # Step 5: Convert JSON to DOCX using style 5
        print("\n=== Step 5: Converting to DOCX (Style 5) ===")
        resume_directory = "generated_resumes"
        os.makedirs(resume_directory, exist_ok=True)
        
        from document_creation import generate_resume_style_5
        docx_resume_path = generate_resume_style_5(json_resume_path, resume_directory)
        
        if not docx_resume_path or not os.path.exists(docx_resume_path):
            return jsonify({'error': 'Failed to create resume document'}), 500
        
        print(f"✅ Resume DOCX created at: {docx_resume_path}")
        return jsonify({'resume_path': docx_resume_path, 'success': True}), 200
        
    except Exception as e:
        print(f"❌ Error creating resume: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app2.route('/send_email', methods=['POST'])
def send_email():
    """Send email with resume attachment using EmailSender class"""
    temp_path = None
    try:
        # Get form data
        recruiter_name = request.form.get('recruiter_name', 'Hiring Manager')
        recruiter_email = request.form.get('recruiter_email')
        subject = request.form.get('subject', 'Application for Position')
        body = request.form.get('body', '')
        resume_file = request.files.get('resume')
        resume_path = request.form.get('resume_path', '')
        
        if not recruiter_email:
            return jsonify({'success': False, 'error': 'Recruiter email is required'}), 400
        
        if not body:
            return jsonify({'success': False, 'error': 'Email body is required'}), 400
        
        # Handle resume attachment - check for server-side path or uploaded file
        if resume_path and os.path.exists(resume_path):
            # Use the server-side generated resume
            email_sender_2.resume_file = resume_path
            email_sender_2._original_filename = os.path.basename(resume_path)
            attach_resume = True
        elif resume_file:
            # Save uploaded resume temporarily
            from datetime import datetime
            original_filename = resume_file.filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_filename = f"resume_{timestamp}_{original_filename}"
            temp_path = os.path.join(os.getcwd(), temp_filename)
            resume_file.save(temp_path)
            
            # Override filename in EmailSender to use original name
            email_sender_2.resume_file = temp_path
            email_sender_2._original_filename = original_filename
            attach_resume = True
        else:
            attach_resume = False
        
        # Use EmailSender class to send email
        success = email_sender_2.send_email(
            recruiter_email=recruiter_email,
            recruiter_name=recruiter_name,
            subject=subject,
            body=body,
            attach_resume=attach_resume
        )
        
        if success:
            print(f"✅ Email sent successfully to {recruiter_email}")
            return jsonify({'success': True, 'message': 'Email sent successfully'}), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to send email'}), 500
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        # Clean up temp file if created
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        if hasattr(email_sender_2, '_original_filename'):
            delattr(email_sender_2, '_original_filename')

if __name__ == '__main__':
    app2.run(debug=True, host='0.0.0.0', port=5003)

