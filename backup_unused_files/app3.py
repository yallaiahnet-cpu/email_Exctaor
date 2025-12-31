from flask import Flask, request, jsonify, render_template
import json
import re
import os
from datetime import datetime
from dotenv import load_dotenv
from cleaning_jd import EmailExtractor
from send_email import EmailSender
from llm_exctration import ResumeOptimizer

# Load environment variables
load_dotenv()

app3 = Flask(__name__)

# Initialize EmailSender for third email account (port 5004)
SMTP_USERNAME_3 = os.getenv('SMTP_USERNAME_3', '')
SMTP_PASSWORD_3 = os.getenv('SMTP_PASSWORD_3', '')
RESUME_FILE_3 = os.getenv('PDF_RESUME_PATH_3', '')

email_sender_3 = EmailSender(
    sender_email=SMTP_USERNAME_3,
    app_password=SMTP_PASSWORD_3,
    resume_file=RESUME_FILE_3
)

@app3.route('/')
def index():
    return render_template('index.html')

@app3.route('/clean_job_description', methods=['POST'])
def clean_job_description():
    try:
        # Get input from frontend
        raw_text = request.get_json()['raw_text']

        # Use profile 2 or 1 as needed; keeping consistent with app2's alternate profile
        extractor = EmailExtractor(raw_text, use_profile_2=True)
        result_json = extractor.extract_email_info_from_jd(raw_text)

        # Try to parse JSON directly first
        try:
            result_dict = json.loads(result_json)
            return jsonify(result_dict), 200
        except json.JSONDecodeError:
            # Extract JSON and try to fix it
            json_match = re.search(r'\{.*\}', result_json, re.DOTALL)
            if json_match:
                cleaned_json = json_match.group(0)
                # Try multiple parsing strategies
                for strategy in ['direct', 'replace_all']:
                    try:
                        if strategy == 'direct':
                            result_dict = json.loads(cleaned_json)
                        elif strategy == 'replace_all':
                            fixed_json = cleaned_json.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                            result_dict = json.loads(fixed_json)
                        return jsonify(result_dict), 200
                    except json.JSONDecodeError:
                        continue
            return jsonify({'error': 'No valid JSON found in response'}), 500
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to parse JSON: {str(e)}'}), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app3.route('/list_resumes', methods=['GET'])
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

@app3.route('/create_resume', methods=['POST'])
def create_resume():
    """Create optimized resume using ResumeOptimizer and convert to DOCX"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '')

        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400

        optimizer = ResumeOptimizer(job_description)

        # Extract skills (not directly used but keeps logs consistent)
        _ = optimizer.extract_skills()

        # Generate optimized resume JSON
        optimizer.generate_resume()

        if not optimizer.resume_json:
            return jsonify({'error': 'Failed to generate resume JSON'}), 500

        # Ensure JSON is proper dict
        if isinstance(optimizer.resume_json, str):
            optimizer.resume_json = json.loads(optimizer.resume_json)
        json.dumps(optimizer.resume_json)

        # Save JSON
        output_dir = "resumes"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"optimized_resume_{timestamp}.json"
        json_resume_path = os.path.join(output_dir, json_filename)
        with open(json_resume_path, 'w') as f:
            json.dump(optimizer.resume_json, f, indent=2)

        # Convert JSON to DOCX using style 5
        from document_creation import generate_resume_style_5
        resume_directory = "generated_resumes"
        os.makedirs(resume_directory, exist_ok=True)
        docx_resume_path = generate_resume_style_5(json_resume_path, resume_directory)

        if not docx_resume_path or not os.path.exists(docx_resume_path):
            return jsonify({'error': 'Failed to create resume document'}), 500

        return jsonify({'resume_path': docx_resume_path, 'success': True}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app3.route('/send_email', methods=['POST'])
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

        # Handle resume attachment
        if resume_path and os.path.exists(resume_path):
            email_sender_3.resume_file = resume_path
            email_sender_3._original_filename = os.path.basename(resume_path)
            attach_resume = True
        elif resume_file:
            original_filename = resume_file.filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_filename = f"resume_{timestamp}_{original_filename}"
            temp_path = os.path.join(os.getcwd(), temp_filename)
            resume_file.save(temp_path)

            email_sender_3.resume_file = temp_path
            email_sender_3._original_filename = original_filename
            attach_resume = True
        else:
            attach_resume = False

        success = email_sender_3.send_email(
            recruiter_email=recruiter_email,
            recruiter_name=recruiter_name,
            subject=subject,
            body=body,
            attach_resume=attach_resume
        )

        if success:
            return jsonify({'success': True, 'message': 'Email sent successfully'}), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to send email'}), 500

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        if hasattr(email_sender_3, '_original_filename'):
            delattr(email_sender_3, '_original_filename')

if __name__ == '__main__':
    app3.run(debug=True, host='0.0.0.0', port=5004)


