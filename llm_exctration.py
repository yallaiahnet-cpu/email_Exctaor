import os
import json
import re
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

# Load environment variables first
load_dotenv()

try:
    from stroup import strouptparse
except ImportError:
    # Provide a fallback or error if strouptparse is unavailable
    def strouptparse(value):
        # Try to get JSON object from string using regex or fallback to original string
        try:
            json_match = re.search(r'({.*?})', value, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            # Fallback: try loading any JSON in string
            return json.loads(value)
        except Exception:
            return value

# Initialize Cohere model lazily - will be created when needed
cohere_model = None

def get_cohere_model():
    """Lazily initialize and return the Cohere model"""
    global cohere_model
    if cohere_model is None:
        try:
            cohere_model = init_chat_model("command-a-03-2025", model_provider="cohere")
        except Exception as e:
            logging.error(f"Failed to initialize Cohere model: {e}")
            cohere_model = None
    return cohere_model

class ResumeOptimizer:
    """
    A robust class to optimize resumes based on job descriptions using LLM.
    
    Usage:
        optimizer = ResumeOptimizer(job_description)
        resume_file_path = optimizer.workflow()
    """
     
    def __init__(self, job_description):
        """
        Initialize the ResumeOptimizer with a job description.
        
        Args:
            job_description (str): The job description to optimize the resume for
        """
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.info_log = logging.info
        self.error_log = logging.error
        
        # Initialize Groq model
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            logging.warning("GROQ_API_KEY not found in environment")
            self.groq_model = None
        else:
            try:
                self.groq_model = ChatGroq(
                    model="llama-3.1-8b-instant",
                    temperature=0.7,
                    streaming=False,
                    api_key=groq_key
                )
                logging.info("Groq model initialized successfully")
            except Exception as e:
                logging.warning(f"Failed to initialize Groq model: {e}")
                self.groq_model = None
        
        # Store job description
        self.job_description = job_description
        
        # Initialize variables to store intermediate results
        self.extracted_skills = None
        self.resume_json = None
    
    def extract_skills(self):
        """Extract skills from job description using LLM and then parse using strouptparse"""
        try:
            cleaned_jd = self.job_description.strip()
            messages = [
                SystemMessage(content=("""
                   You are an expert technical recruiter and hiring manager.
                        Analyze the job description below and return a structured analysis to assess candidate fit.
                        there are so many unwanted words in the job description, so you need to extract the skills from the job description.

                        Extract the following:

                        1. Business Context

                        * Company domain: What the company does
                        * Role focus: What problem this role solves
                        * Team structure: Who this role collaborates with or reports to

                        2. Technical Skills

                        * Explicitly Required: Skills and technologies exactly as written in the JD
                        * Inferred Skills (with justification): Skills standard for this role type but not mentioned; justify each

                        3. Tools and Technologies

                        * Explicitly Mentioned: Tools/platforms exactly as written
                        * Commonly Expected (inferred): Standard tools based on the role's domain or workflows; justify each

                        4. Experience Requirements

                        * Extract years of experience, education, and proficiency indicators

                        5. Soft Skills

                        * Explicit: Directly stated soft skills
                        * Inferred: Implied soft skills based on wording or responsibilities

                        6. Key Phrases Indicating Culture/Priorities

                        * Extract exact phrases from the JD that reflect company values

                        7. Good to Mention (Missing but Valuable)
                        List expected but missing tools, practices, or skills

                        * Format each as:
                        * \[Item] – \[Why it's commonly expected for this role type]

                        Format your output strictly as YAML:

                        Business Context:
                            Company domain:
                            Role focus:
                            Team structure:

                        Technical Skills:
                            Explicitly Required:
                                -
                            Inferred Skills (with justification):
                                -

                        Tools and Technologies:
                            Explicitly Mentioned:
                                -
                            Commonly Expected (inferred):
                                -

                        Experience Requirements:
                            -  number of years of experience 

                        Soft Skills:
                            Explicit:
                                -
                            Inferred:
                                -

                        Key Phrases Indicating Culture/Priorities:
                            -

                        Good to Mention (Missing but Valuable):
                            -
                    mine is artificial intilligence and machine leraning so mcp means model context protocal, a2a means agent to agnet comunucation.
                    """
                )),
                HumanMessage(content=cleaned_jd),
            ]
            extract_skills = self.groq_model.invoke(messages)
            # Extract content from response
            if hasattr(extract_skills, 'content'):
                raw_content = extract_skills.content
            elif hasattr(extract_skills, 'message') and hasattr(extract_skills.message, 'content'):
                raw_content = extract_skills.message.content
            else:
                raw_content = str(extract_skills)
            # Use strouptparse after llm invoke
            try:
                self.extracted_skills = strouptparse(raw_content)
            except Exception as e:
                self.error_log(f"Error parsing LLM skills output with strouptparse: {e}")
                self.extracted_skills = raw_content
            return self.extracted_skills
        except Exception as e:
            self.error_log(f"Error in LLM skills extraction: {e}")
            return f"Error extracting skills: {str(e)}"
    
    def generate_resume(self):
        """Generate optimized resume based on extracted skills, and parse with strouptparse after llm invoke"""
        try:
            if not self.groq_model:
                raise Exception("Groq model not initialized")
            if not self.extracted_skills:
                self.extract_skills()
            
            # Essential rules from SYSTEM_PROMPT
            SYSTEM_PROMPT = """
    You are an ATS resume optimizer trained to generate resumes that score 100% on applicant tracking systems. 

Return ONLY optimized JSON output — no comments, no explanations, and no extra text.

------------------------------------------------------------
INSTRUCTIONS
------------------------------------------------------------
Output: Valid JSON resume ONLY. No markdown or formatting hints.

Goal: Create a fully customized, JD-specific, ATS-optimized resume strictly following all rules.

------------------------------------------------------------
    SECTION RULES
------------------------------------------------------------
    PERSONAL INFO
• Change title to best match JD.

    SUMMARY
• 18 bullet points, each 230–280 characters in health care domin, insurance domain.
• Integrate JD keywords with candidate’s experience (Insurance, Healthcare, Banking, Consulting).

------------------------------------------------------------
PROFESSIONAL EXPERIENCE (CLIENTS 1–5)
------------------------------------------------------------
For each client role:
• Keep original role title.
• Follow bullet count & length:
  -- stricly every bullet point must 300 to 320 characters long.
  - Client 1: 16 bullets (Insurance)
  - Client 2: 14 bullets (Healthcare)
  - Client 3: 12 bullets (Healthcare)
  - Client 4: 10 bullets (Banking)
  - Client 5: 8 bullets (Consulting)
• 230–280 characters per bullet.
• 70% bullets follow format:
  [Technology/Tool] + [Problem] + [Solution/Action] + [Impact].(note impact is not mention in numaric format like 70% or 80% or 90% or 100% etc. just mention the impact in words.)
• Integrate JD skills/tools.
• Use cloud as per JD; if absent, default by client:
  - Client 1 & 2 → AWS
  - Client 3 → GCP keep the gcp only,   even though the jd is not mentioning the gcp.
  - Client 4 & 5 → Azure keep the azure only even though the jd is not mentioning the azure.
• No multi-cloud mention.
• Match technology to real adoption timelines.
• Use domain compliance terms (HIPAA, PCI, GDPR) where relevant.
• Show real tasks: debugging, meetings, code reviews, troubleshooting.
• Avoid filler, buzzwords, or AI-like phrasing.
• Maintain authenticity, show emotions, learning, and trial/error.
• Vary action verbs; no verb repetition.
• Show career progression through verb complexity (junior → senior).
• Reflect realistic developer challenges and mundane tasks.
• Maintain human tone with personal context (“I struggled with…”, “Had to learn…”).

------------------------------------------------------------
TECH TIMELINE & CLOUD RULES
------------------------------------------------------------
• Respect real-world adoption years.
• Early (2010–2015): On-prem, monoliths.
• Mid (2015–2020): Cloud migration, microservices.
• Recent (2020+): Cloud-native, serverless, orchestration.
• Maintain HIPAA compliance for healthcare projects.

------------------------------------------------------------
    CERTIFICATIONS
------------------------------------------------------------
• Keep existing ones unchanged; do not add new.

------------------------------------------------------------
TOOL & TECH SECTIONS
------------------------------------------------------------
• 10–12 categories max (Languages, ML, Cloud, Big Data, Databases, etc.)
• Realistic mapping based on project timelines. each section catogory is must be 4 to 20 skills.
• CRITICAL: Keep ALL technical skills EXACTLY as provided in the template - DO NOT add, remove, or modify ANY skills.
• The technical_skills section must remain IDENTICAL to the template with all original skills preserved.

------------------------------------------------------------
LANGUAGE & STYLE RULES
------------------------------------------------------------
Tone:
• Conversational, Indian tone, authentic.
• Include imperfections, learning curves, and team collaboration.
• Avoid buzzwords like “robust”, “cutting-edge”, “expert”.
• Use natural, casual connectors (“Actually”, “Plus”, “Basically”).
• Include minor struggles and relatable developer emotions.

Structure:
• Every bullet unique in verb choice.
• No corporate or AI phrasing.
• Keep actions human and specific, not abstract.
• Mention mundane details (bug fixes, meetings, testing).

Writing Style:
1. Add imperfection and learning moments.
2. Use contractions naturally.
3. Reflect growth and realistic career progression.
4. Include team interactions.
5. Vary sentence length.
6. Avoid metric percentages unless originally present.
7. Include approximate numbers only if natural (“around”, “roughly”).
8. Remove all generic corporate terms.
9. Express actions through specific outcomes.
10. Add emotional realism (“frustrating but worth it”, “took me a while”).

------------------------------------------------------------
JD INTEGRATION RULES
------------------------------------------------------------
• Integrate 4–6 JD skills naturally across sections.
• Show progression in using these tools.
• Use authentic project-based application examples.
• Add 4–5 more realistic related skills to strengthen alignment.

------------------------------------------------------------
PROHIBITED TERMS
------------------------------------------------------------
Never use: Adept, Self-starter, Championed, Specialized, Proven track record, Expert, Advanced, Cutting-edge, Leveraged, Robust, Key player, Instrumental, Mastery, Well-versed, Results-driven, Detail-oriented, Team player, Strategic, Exceptional, Outstanding, Value-added, Game-changer, World-class, Industry-leading, Mission-critical, Holistic.

------------------------------------------------------------
APPROVED ACTION VERBS
------------------------------------------------------------
Built, Engineered, Deployed, Assembled, Used, Utilized, Applied, Integrated, Operationalized, Collaborated, Aligned with, Partnered with, Contributed, Delivered, Created, Developed, Produced, Helped, Assisted, Supported, Facilitated, Got, Achieved, Obtained, Secured, Worked with, Coordinated, Led, Mentored, Guided, Orchestrated, Architected, Implemented, Executed, Set up, Deployed, Configured, Automated, Updated, Modernized, Transformed, Enhanced, Improved, Streamlined.

------------------------------------------------------------
EXECUTION CHECKLIST
------------------------------------------------------------
• Exact bullet counts & lengths.
• Tech timeline validated.
• JD keywords integrated.
• Career growth visible.
• Realistic domain details (HIPAA, PCI).
• No multi-cloud.
• Human tone maintained.
• No numeric percentages.
• Technical skills preserved EXACTLY as in template - NO changes allowed.
• Output only valid JSON resume.

------------------------------------------------------------
FINAL OUTPUT FORMAT
------------------------------------------------------------
Return a complete JSON resume artifact with:
- Personal Info
- Summary (18 bullets)
- stricly every bullet point must 300 to 320 characters long.
- Experience (Client 1–5 with correct counts)
- Technical Skills (10–12 categories)
- Certifications
- Strictly do not mention any metrics like 70% like below 
    example :-•	Built a client portal using React.js, integrating RESTful APIs for data management, which improved user engagement by roughly 25%.
Do NOT include any extra commentary, markdown, or formatting beyond valid JSON.

------------------------------------------------------------
INPUT FORMAT
------------------------------------------------------------
JOB_DESCRIPTION: Structured skills list from JD  
RESUME_JSON: Candidate’s raw resume data  



    {
      "name": "Yallaiah Onteru",
      "title": "",
      "contact": {
        "email": "yonteru.dev.ai@gmail.com",
        "phone": "9733271133",
        "portfolio": "",
        "linkedin": "https://www.linkedin.com/in/yalleshaiengineer/",
        "github": ""
      },
      "professional_summary": [
        "[Bullet Point 1]",
        "[Bullet Point 2]",
        "[Bullet Point 3]",
        "[Bullet Point 4]",
        "[Bullet Point 5]",
        "[Bullet Point 6]",
        "[Bullet Point 7]",
        "[Bullet Point 8]",
        "[Bullet Point 9]",
        "[Bullet Point 10]",
        "[Bullet Point 11]",
        "[Bullet Point 12]",
        "[Bullet Point 13]",
        "[Bullet Point 14]",
        "[Bullet Point 15]",
        "[Bullet Point 16]",
        "[Bullet Point 17]",
        "[Bullet Point 18]"
      ],
      "technical_skills": {
        "Programming Languages": [
          "Python", "R", "Java", "SQL", "Scala", "Bash/Shell", "TypeScript"
        ],
        "Machine Learning Models": [
          "Scikit-Learn", "TensorFlow", "PyTorch", "Keras", "XGBoost", "LightGBM", "H2O", "AutoML", "Mllib"
        ],
        "Deep Learning Models": [
          "Convolutional Neural Networks (CNNs)", "Recurrent Neural Networks (RNNs)", "LSTMs", "Transformers", "Generative Models", "Attention Mechanisms", "Transfer Learning", "Fine-tuning LLMs"
        ],
        "Statistical Techniques": [
          "A/B Testing", "ANOVA", "Hypothesis Testing", "PCA", "Factor Analysis", "Regression (Linear, Logistic)", "Clustering (K-Means)", "Time Series (Prophet)"
        ],
        "Natural Language Processing": [
          "spaCy", "NLTK", "Hugging Face Transformers", "BERT", "GPT", "Stanford NLP", "TF-IDF", "LSI", "Lang Chain", "Llama Index", "OpenAI APIs", "MCP", "RAG Pipelines", "Crew AI", "Claude AI"
        ],
        "Data Manipulation & Visualization": [
          "Pandas", "NumPy", "SciPy", "Dask", "Apache Arrow", "seaborn", "matplotlib", "Seaborn", "Plotly", "Bokeh", "ggplot2", "Tableau", "Power BI", "D3.js"
        ],
        "Big Data Frameworks": [
          "Apache Spark", "Apache Hadoop", "Apache Flink", "Apache Kafka", "HBase", "Spark Streaming", "Hive", "MapReduce", "Databricks", "Apache Airflow", "dbt"
        ],
        "ETL & Data Pipelines": [
          "Apache Airflow", "AWS Glue", "Azure Data Factory", "Informatica", "Talend", "Apache NiFi", "Apache Beam", "Informatica PowerCenter", "SSIS"
        ],
        "Cloud Platforms": [
          "AWS (S3, SageMaker, Lambda, EC2, RDS, Redshift, Bedrock)", "Azure (ML Studio, Data Factory, Databricks, Cosmos DB)", "GCP (Big Query, Vertex AI, Cloud SQL)"
        ],
        "Web Technologies": [
          "REST APIs", "Flask", "Django", "Fast API", "React.js"
        ],
        "Statistical Software": [
          "R (dplyr, caret, ggplot2, tidyr)", "SAS", "STATA"
        ],
        "Databases": [
          "PostgreSQL", "MySQL", "Oracle", "Snowflake", "MongoDB", "Cassandra", "Redis", "Snowflake Elasticsearch", "AWS RDS", "Google Big Query", "SQL Server", "Netezza", "Teradata"
        ],
        "Containerization & Orchestration": [
          "Docker", "Kubernetes"
        ],
        "MLOps & Deployment": [
          "ML flow", "DVC", "Kubeflow", "Docker", "Kubernetes", "Flask", "Fast API", "Streamlit"
        ],
        "Streaming & Messaging": [
          "Apache Kafka", "Spark Streaming", "Amazon Kinesis"
        ],
        "DevOps & CI/CD": [
          "Git", "GitHub", "GitLab", "Bitbucket", "Jenkins", "GitHub Actions", "Terraform"
        ],
        "Development Tools": [
          "Jupyter Notebook", "VS Code", "PyCharm", "RStudio", "Google Colab", "Anaconda"
        ]
      },
      "experience": [
        {
          "role": "AI Lead Engineer",
          "client": "State Farm",
          "duration": "2025-Jan - Present",
          "location": "Austin, Texas.",
          "responsibilities": [
            "[Bullet Point 1]",
            "[Bullet Point 2]",
            "[Bullet Point 3]",
            "[Bullet Point 4]",
            "[Bullet Point 5]",
            "[Bullet Point 6]",
            "[Bullet Point 7]",
            "[Bullet Point 8]",
            "[Bullet Point 9]",
            "[Bullet Point 10]",
            "[Bullet Point 11]",
            "[Bullet Point 12]",
            "[Bullet Point 13]",
            "[Bullet Point 14]",
            "[Bullet Point 15]",
            "[Bullet Point 16]"
          ],
          "environment": [
            "[Technology stack will be populated from JD]"
          ]
        },
        {
          "role": "Senior AI Engineer",
          "client": "Johnson & Johnson",
          "duration": "2021-Aug - 2024-Dec",
          "location": "New Brunswick, New Jersey.",
          "responsibilities": [
            "[Bullet Point 1]",
            "[Bullet Point 2]",
            "[Bullet Point 3]",
            "[Bullet Point 4]",
            "[Bullet Point 5]",
            "[Bullet Point 6]",
            "[Bullet Point 7]",
            "[Bullet Point 8]",
            "[Bullet Point 9]",
            "[Bullet Point 10]",
            "[Bullet Point 11]",
            "[Bullet Point 12]",
            "[Bullet Point 13]",
            "[Bullet Point 14]"
          ],
          "environment": [
            "[Technology stack will be populated from JD]"
          ]
        },
        {
          "role": "Senior ML Engineer",
          "client": "State of Maine",
          "duration": "2020-Apr - 2021-Jul",
          "location": "Augusta, Maine.",
          "responsibilities": [
            "[Bullet Point 1]",
            "[Bullet Point 2]",
            "[Bullet Point 3]",
            "[Bullet Point 4]",
            "[Bullet Point 5]",
            "[Bullet Point 6]",
            "[Bullet Point 7]",
            "[Bullet Point 8]",
            "[Bullet Point 9]",
            "[Bullet Point 10]",
            "[Bullet Point 11]",
            "[Bullet Point 12]"
          ],
          "environment": [
            "[Technology stack will be populated from JD]"
          ]
        },
        {
          "role": "Data Scientist",
          "client": "Bank of America",
          "duration": "2018-Jan - 2020-Mar",
          "location": " New York, New York.",
          "responsibilities": [
            "[Bullet Point 1]",
            "[Bullet Point 2]",
            "[Bullet Point 3]",
            "[Bullet Point 4]",
            "[Bullet Point 5]",
            "[Bullet Point 6]",
            "[Bullet Point 7]",
            "[Bullet Point 8]",
            "[Bullet Point 9]",
            "[Bullet Point 10]"
          ],
          "environment": [
            "[Technology stack will be populated from JD]"
          ]
        },
        {
          "role": "Data Engineer",
          "client": "Hexaware",
          "duration": "2015-Oct - 2017-Dec",
          "location": "Mumbai, Maharashtra.",
          "responsibilities": [
            "[Bullet Point 1]",
            "[Bullet Point 2]",
            "[Bullet Point 3]",
            "[Bullet Point 4]",
            "[Bullet Point 5]",
            "[Bullet Point 6]",
            "[Bullet Point 7]",
            "[Bullet Point 8]"
          ],
          "environment": [
            "[Technology stack will be populated from JD]"
          ]
        }
      ],
      "education": [
        {
          "institution": "KITS",
          "degree": "B.Tech",
          "field": "Computer Science",
          "year": "2015"
        }
      ],
      "certifications": [
        "Microsoft Certified: Azure Data Engineer Associate",
        "Microsoft Certified: Azure AI Engineer Associate",
        "AWS Certified Machine Learning Engineer – Associate",
        "Salesforce Certified Salesforce Developer PD1 "
      ]
    }
    """
            
            
            combined_messages = [
                SystemMessage(content=f"{SYSTEM_PROMPT}"),
                HumanMessage(content=f"Job Description:\n{self.job_description[:1800]}\n\nGenerate optimized resume JSON following ALL rules above. Return ONLY valid JSON.")
            ]
            # Try Cohere model first, fallback to Groq if not available
            cohere_model = get_cohere_model()
            if cohere_model is not None:
                final_response = cohere_model.invoke(combined_messages)
            elif self.groq_model is not None:
                final_response = self.groq_model.invoke(combined_messages)
            else:
                error_msg = "Neither Cohere nor Groq model is available. "
                error_msg += "Please set CO_API_KEY (for Cohere) or GROQ_API_KEY (for Groq) environment variable."
                raise Exception(error_msg)
            # Extract content from response
            if hasattr(final_response, 'content'):
                raw_response = final_response.content
            elif hasattr(final_response, 'message') and hasattr(final_response.message, 'content'):
                raw_response = final_response.message.content
            else:
                raw_response = str(final_response)
            # Use strouptparse after llm invoke for resume
            try:
                self.resume_json = strouptparse(raw_response)
            except Exception as e:
                self.error_log(f"Error parsing LLM resume output with strouptparse: {e}")
                # Fallback: naive clean and JSON load
                try:
                    cleaned_json = self.clean_json_response(raw_response)
                    self.resume_json = json.loads(cleaned_json)
                except Exception as ex:
                    self.error_log(f"Error in fallback clean_json_response: {ex}")
                    self.resume_json = raw_response
            
            # CRITICAL: Force restore original technical skills to ensure they are never modified by AI
            self._restore_original_technical_skills()
            
            return self.resume_json
        except Exception as e:
            self.error_log(f"Error in LLM final response: {e}")
            return f"Error generating final response: {str(e)}"
    
    def _restore_original_technical_skills(self):
        """Force restore the original technical skills from the template to prevent AI modifications"""
        if not self.resume_json or not isinstance(self.resume_json, dict):
            return
        
        # Original technical skills from the template
        original_skills = {
            "Programming Languages": [
                "Python", "R", "Java", "SQL", "Scala", "Bash/Shell", "TypeScript"
            ],
            "Machine Learning Models": [
                "Scikit-Learn", "TensorFlow", "PyTorch", "Keras", "XGBoost", "LightGBM", "H2O", "AutoML", "Mllib"
            ],
            "Deep Learning Models": [
                "Convolutional Neural Networks (CNNs)", "Recurrent Neural Networks (RNNs)", "LSTMs", "Transformers", "Generative Models", "Attention Mechanisms", "Transfer Learning", "Fine-tuning LLMs"
            ],
            "Statistical Techniques": [
                "A/B Testing", "ANOVA", "Hypothesis Testing", "PCA", "Factor Analysis", "Regression (Linear, Logistic)", "Clustering (K-Means)", "Time Series (Prophet)"
            ],
            "Natural Language Processing": [
                "spaCy", "NLTK", "Hugging Face Transformers", "BERT", "GPT", "Stanford NLP", "TF-IDF", "LSI", "Lang Chain", "Llama Index", "OpenAI APIs", "MCP", "RAG Pipelines", "Crew AI", "Claude AI"
            ],
            "Data Manipulation & Visualization": [
                "Pandas", "NumPy", "SciPy", "Dask", "Apache Arrow", "seaborn", "matplotlib", "Seaborn", "Plotly", "Bokeh", "ggplot2", "Tableau", "Power BI", "D3.js"
            ],
            "Big Data Frameworks": [
                "Apache Spark", "Apache Hadoop", "Apache Flink", "Apache Kafka", "HBase", "Spark Streaming", "Hive", "MapReduce", "Databricks", "Apache Airflow", "dbt"
            ],
            "ETL & Data Pipelines": [
                "Apache Airflow", "AWS Glue", "Azure Data Factory", "Informatica", "Talend", "Apache NiFi", "Apache Beam", "Informatica PowerCenter", "SSIS"
            ],
            "Cloud Platforms": [
                "AWS (S3, SageMaker, Lambda, EC2, RDS, Redshift, Bedrock)", "Azure (ML Studio, Data Factory, Databricks, Cosmos DB)", "GCP (Big Query, Vertex AI, Cloud SQL)"
            ],
            "Web Technologies": [
                "REST APIs", "Flask", "Django", "Fast API", "React.js"
            ],
            "Statistical Software": [
                "R (dplyr, caret, ggplot2, tidyr)", "SAS", "STATA"
            ],
            "Databases": [
                "PostgreSQL", "MySQL", "Oracle", "Snowflake", "MongoDB", "Cassandra", "Redis", "Snowflake Elasticsearch", "AWS RDS", "Google Big Query", "SQL Server", "Netezza", "Teradata"
            ],
            "Containerization & Orchestration": [
                "Docker", "Kubernetes"
            ],
            "MLOps & Deployment": [
                "ML flow", "DVC", "Kubeflow", "Docker", "Kubernetes", "Flask", "Fast API", "Streamlit"
            ],
            "Streaming & Messaging": [
                "Apache Kafka", "Spark Streaming", "Amazon Kinesis"
            ],
            "DevOps & CI/CD": [
                "Git", "GitHub", "GitLab", "Bitbucket", "Jenkins", "GitHub Actions", "Terraform"
            ],
            "Development Tools": [
                "Jupyter Notebook", "VS Code", "PyCharm", "RStudio", "Google Colab", "Anaconda"
            ]
        }
        
        # Force restore original skills
        self.resume_json['technical_skills'] = original_skills
        self.info_log("✅ Restored original technical skills to prevent AI modifications")
    
    def clean_json_response(self, raw_response):
        """Clean and extract JSON from LLM response"""
        try:
            # Remove markdown code blocks if present
            json_match = re.search(r'```json\s*(.*?)\s*```', raw_response, re.DOTALL)
            if json_match:
                return json_match.group(1).strip()
            
            # Look for JSON object in the response
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                return json_match.group(0).strip()
            
            # If no JSON found, return as is (will raise error in parsing)
            return raw_response.strip()
        except Exception as e:
            self.error_log(f"Error cleaning JSON response: {e}")
            return raw_response
    
    def create_document(self):
        """Create a document from the resume JSON and return the file path"""
        try:
            if not self.resume_json:
                self.generate_resume()
            
            # Create output directory if it doesn't exist
            output_dir = "resumes"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"optimized_resume_{timestamp}.json"
            file_path = os.path.join(output_dir, filename)
            
            # Write JSON to file
            with open(file_path, 'w') as f:
                json.dump(self.resume_json, f, indent=2)
            
            self.info_log(f"Resume saved to: {file_path}")
            return file_path
        except Exception as e:
            self.error_log(f"Error creating document: {e}")
            return None
    
    def workflow(self):
        """
        Execute the complete workflow: extract skills, generate resume, and create document.
        
        Returns:
            str: Path to the generated resume document
        """
        try:
            self.info_log("Starting resume optimization workflow")
            
            # Step 1: Extract skills from job description
            self.info_log("Extracting skills from job description")
            self.extract_skills()
            
            # Step 2: Generate optimized resume
            self.info_log("Generating optimized resume")
            self.generate_resume()
            
            # Step 3: Create document
            self.info_log("Creating resume document")
            file_path = self.create_document()
            
            self.info_log("Resume optimization workflow completed successfully")
            return file_path
        except Exception as e:
            self.error_log(f"Error in workflow: {e}")
            return None


# Example usage
if __name__ == "__main__":
   print("reume optimiser")