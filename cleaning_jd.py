import json
import logging
import os
import re
from typing import Any, Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# Load environment variables for Groq
load_dotenv()

# Initialize Groq model lazily to avoid proxy issues
groq_model = None
try:
    groq_model = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        streaming=False,
        api_key=os.getenv("GROQ_API_KEY")
    )
except Exception as e:
    logging.warning(f"Failed to initialize Groq model: {e}")
    groq_model = None

parser = StrOutputParser()


class EmailExtractor:
    """
    Use an LLM to understand recruiter/job-posting text and craft a tailored reply.
    """

    def __init__(self, email_text: str, use_profile_2: bool = False, years_of_experience: str = "10+ years"):
        self.email_text = email_text
        self.use_profile_2 = use_profile_2
        self.years_of_experience = years_of_experience

    def extract_email_info_from_jd(self, cleaned_jd: str) -> str:
        try:
            years_exp = self.years_of_experience
            system_prompt = f"""
            You are an expert technical recruiter assistant. Analyze the input text (job description, recruiter email, LinkedIn message, or other hiring communication) and perform TWO tasks.

            STEP 1: Determine the communication intent of the text. Choose one of:
                - recruiter_outreach: A recruiter or hiring manager reached out directly (LinkedIn/Email/InMail) to the candidate.
                - job_posting: A job description or posting where the candidate is initiating contact.
                - other: Any other context (follow-ups, referrals, unclear scenarios). Treat like job_posting for email drafting.
            Output the selected value under the "intent" key in the final JSON.

            STEP 2: Extract recruiter information and create an appropriate reply email based on the detected intent.

            Recruiter Info (always attempt to fill):
                - name: Recruiter's full name (if available).
                - email: Recruiter/Hiring email explicitly listed in the text. Do NOT invent emails.

            Subject line rules:
                - ALWAYS use this detailed format regardless of intent: "[Job Title] – [Key Tech 1 | Key Tech 2 | Key Tech 3 | ...] | [Location] | [Work Arrangement]"
                    - Extract 5-7 most important technologies/frameworks from the job description
                    - PRIORITY ORDER: If cloud services (AWS, Azure, GCP, Google Cloud) or infrastructure platforms are mentioned, list them FIRST, then other technologies
                      * Examples: "AWS | Azure | Python | PySpark | SQL | Microsoft Fabric | AI Foundry" (if AWS and Azure are mentioned)
                      * Examples: "Python | PyTorch | TensorFlow | LangChain" (if no cloud service is mentioned)
                    - Common technologies to extract: AWS, Azure, GCP, AWS Bedrock, LangGraph, LangChain, Python, PySpark, SQL, Microsoft Fabric, AI Foundry, TypeScript, JavaScript, PyTorch, TensorFlow, etc.
                    - Extract location(s) - if multiple, use "/" to separate (e.g., "Malvern/Charlotte")
                    - If location is "San Jose- CA" or similar, use "Remote, USA" or the actual location mentioned
                    - Determine work arrangement from keywords:
                      * "onsite", "on-site", "on site", "must be onsite", "in-office" → "ONSITE"
                      * "remote", "work from home", "WFH", "fully remote", "Remote" → "REMOTE"
                      * "hybrid", "partially remote", "flexible" → "HYBRID"
                      * If multiple options mentioned, use "ONSITE OR REMOTE OR HYBRID" or combine as appropriate
                      * If unclear or if "Onsite at Remote" is mentioned, default to "REMOTE"
                    - Use en dash (–) between job title and technologies, pipe (|) to separate technologies and sections
                    - Examples: 
                      * "Data Engineer – AWS | Azure | Python | PySpark | SQL | Microsoft Fabric | AI Foundry | Remote, USA | REMOTE"
                      * "Generative AI Engineer – AWS | Python | PyTorch | TensorFlow | LangChain | Remote, USA | REMOTE" (AWS mentioned)
                      * "Generative AI Engineer – Python | PyTorch | TensorFlow | LangChain | Remote, USA | REMOTE" (no cloud service)
                      * "Agentic AI Engineer – AWS Bedrock | LangGraph | Python | Malvern/Charlotte | ONSITE"
                    - If location is not specified, use "Remote, USA" as default location
                    - Always include location and work arrangement sections

            Email body requirements (apply to every response):
                - Use professional, simple English.
                - Separate paragraphs with double newlines (\\n\\n).
                - Use the bullet character • for bullet lists.
                - Never include the closing signature (Best Regards, name, phone, email) because the UI appends it.
                - Do NOT use emojis.

            EMAIL BODY FORMATS BY INTENT

            A) When intent == "recruiter_outreach":
                - Start with "Hi [Recruiter Name]," (fallback to "Hi," if no name).
                - Immediately thank them for reaching out (e.g., "Thank you for reaching out about the Senior AI Developer role.").
                - Acknowledge key points from their message (location, skills, client, etc.) when available.
                - Provide a short paragraph confirming interest/availability.
                - Include 2-4 bullet points highlighting relevant strengths/impacts that match the opportunity.
                - Close with a call-to-action such as availability for a chat or request for next steps.
                - Keep tone warm, appreciative, and confident. No humor required.

            B) When intent == "job_posting" or "other":
                - Use the following cheerful outreach template (simple English, light humor):
                "Hello [Recruiter Name],\\n\\nI hope you're doing well [add a light, attention-grabbing line that makes people smile - keep it professional and simple].\\n\\nI'm reaching out because I saw the [Job Title] position and thought - this sounds perfect for me! With over {years_exp} of experience in [broader field], I specialize in **[List 5-8 key skills/technologies from JD]**\\n\\nHere's what I bring to the table:\\n\\n• [Highlight 1]\\n\\n• [Highlight 2]\\n\\n• [Highlight 3]\\n\\n• [Highlight 4]\\n\\nI'm ready to jump in and would love to chat about how I can help your client succeed. My resume is attached - take a look when you get a chance!\\n\\nThank you for reading this [add another light, memorable closing line]. I'm excited about the opportunity to contribute to your client's success!"
                - Humor must remain professional, human, and emoji-free.
                - If no intent can be confidently determined, default to this template.

            Additional humor guidance (only when intent == "job_posting" or "other"):
                - Use very simple English (no complex vocabulary).
                - Add a single warm/funny statement in opening and closing (no sarcasm, no negative jokes).
                - Keep tone friendly and confident.

            Output strictly as JSON (no markdown, no commentary):

            {{
                "intent": "job_posting",
                "recruiter": {{
                    "name": null,
                    "email": null
                }},
                "email": {{
                    "subject": null,
                    "body": null
                }}
            }}
            """

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=cleaned_jd)
            ]

            if groq_model is None or parser is None:
                logging.error("❌ Groq client not available.")
                return json.dumps({
                    "intent": "other",
                    "recruiter": {"name": None, "email": None},
                    "email": {"subject": None, "body": None}
                })

            llm_raw_response = groq_model.invoke(messages)
            parsed_response = parser.invoke(llm_raw_response)
            json_candidate = self.clean_json_response(parsed_response)

            if not self.is_valid_json(json_candidate):
                logging.error("❌ LLM response is not valid JSON.")
                return json_candidate

            parsed_json: dict[str, Any] = json.loads(json_candidate)

            # Normalise intent
            intent = (parsed_json.get('intent') or '').strip().lower()
            if intent not in {"recruiter_outreach", "job_posting", "other"}:
                intent = "job_posting"
                parsed_json['intent'] = intent

            email_section = parsed_json.get('email') or {}
            email_body = email_section.get('body') or ''
            recruiter_info = parsed_json.get('recruiter') or {}
            recruiter_name = (recruiter_info.get('name') or '').strip()

            if email_body:
                if intent == "recruiter_outreach":
                    email_body = self._ensure_prefixed_greeting(email_body, recruiter_name, greeting="Hi")
                else:
                    email_body = self._ensure_prefixed_greeting(email_body, recruiter_name, greeting="Hello")

                # Strip trailing signature text if the model hallucinated any
                email_body = self._strip_signature(email_body)

                # Normalise bullet formatting
                email_body = re.sub(r'^[\s]*[-*+]\s+', '• ', email_body, flags=re.MULTILINE)
                email_body = re.sub(r'•\s*([^\n]+)', r'• \1', email_body)
                email_body = re.sub(r'([^\n])\n• ', r'\1\n\n• ', email_body)

                # Remove markdown bold markers
                email_body = re.sub(r'\*\*([^*]+)\*\*', r'\1', email_body)

                parsed_json['email']['body'] = email_body.strip()

            # Ensure recruiter section exists even if missing
            recruiter_email_clean = (recruiter_info.get('email') or '').strip() or None
            if not recruiter_name and recruiter_email_clean:
                recruiter_name = self._derive_name_from_email(recruiter_email_clean)

            parsed_json['recruiter'] = {
                "name": recruiter_name or None,
                "email": recruiter_email_clean
            }

            return json.dumps(parsed_json, indent=2)
        except Exception as exc:
            logging.error(f"❌ Failed to extract email info: {exc}")
            import traceback
            traceback.print_exc()
            return json.dumps({
                "intent": "other",
                "recruiter": {"name": None, "email": None},
                "email": {"subject": None, "body": None}
            }, indent=2)

    def clean_json_response(self, raw_response: str) -> str:
        """
        Extract JSON from the LLM response, handling fenced code blocks gracefully.
        """
        try:
            json_match = re.search(r'```json\s*(.*?)\s*```', raw_response, re.DOTALL | re.IGNORECASE)
            if json_match:
                return json_match.group(1).strip()

            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                return json_match.group(0).strip()

            return raw_response.strip()
        except Exception as exc:
            logging.error(f"Error cleaning JSON response: {exc}")
            return raw_response

    def is_valid_json(self, text: str) -> bool:
        try:
            json.loads(text)
            return True
        except Exception:
            return False

    @staticmethod
    def _ensure_prefixed_greeting(body: str, name: str, greeting: str = "Hello") -> str:
        """
        Guarantee the email body starts with the requested greeting format.
        """
        body_stripped = body.lstrip()
        name_part = f"{name},"
        if name:
            expected = f"{greeting} {name_part}"
            if re.search(rf'^{greeting}\s+{re.escape(name)}\s*,', body_stripped, re.IGNORECASE):
                return body_stripped
            if re.search(r'^Hello\s+[^,\n]+\s*,', body_stripped, re.IGNORECASE) or re.search(r'^Hi\s+[^,\n]+\s*,', body_stripped, re.IGNORECASE):
                body_stripped = re.sub(r'^(Hello|Hi)\s+[^,\n]+\s*,', f'{greeting} {name},', body_stripped, flags=re.IGNORECASE)
            elif re.match(r'^(Hello|Hi)\s*,', body_stripped, flags=re.IGNORECASE):
                body_stripped = re.sub(r'^(Hello|Hi)\s*,\s*', f'{greeting} {name},\n\n', body_stripped, flags=re.IGNORECASE)
            else:
                body_stripped = f'{greeting} {name},\n\n{body_stripped}'
        else:
            # no name -> generic greeting
            if not re.match(rf'^{greeting}\s*,', body_stripped, flags=re.IGNORECASE):
                body_stripped = re.sub(r'^(Hello|Hi)\s*,', f'{greeting},', body_stripped, flags=re.IGNORECASE)
                if not body_stripped.lower().startswith(f"{greeting.lower()},"):
                    body_stripped = f"{greeting},\n\n{body_stripped}"
        return body_stripped

    @staticmethod
    def _strip_signature(body: str) -> str:
        """
        Remove any trailing signature phrases (Best Regards, Thanks, etc.).
        """
        try:
            lines = body.split('\n')
            cut_idx = None
            for i in range(len(lines) - 1, -1, -1):
                if re.match(r"(?i)^\s*(best\s+regards|regards|thanks\s*&?\s*regards|sincerely)\s*,?\s*$", lines[i] or ""):
                    cut_idx = i
                    break
            if cut_idx is not None:
                return '\n'.join(lines[:cut_idx]).rstrip()
            return body.rstrip()
        except Exception:
            return body.rstrip()

    @staticmethod
    def _derive_name_from_email(email: str) -> Optional[str]:
        """
        Attempt to derive a human-friendly name from an email address.
        Example: "harib@alkaeus.com" -> "Harib"
        """
        try:
            local_part = email.split('@', 1)[0]
            local_part = re.sub(r'[^a-zA-Z\s._-]', ' ', local_part)
            local_part = local_part.replace('.', ' ').replace('_', ' ').replace('-', ' ')
            candidate = ' '.join([w for w in local_part.split() if len(w) > 1])
            if not candidate:
                return None
            candidate = ' '.join(word.capitalize() for word in candidate.split())
            return candidate.strip() or None
        except Exception:
            return None


if __name__ == "__main__":
    sample_text = """
    Austin Richardson
    Lead Delivery Manager at Piper Companies
    Opportunity for a senior ai developer
    Hi Yallaiah,
    I hope this message finds you well! Our client is looking for a Senior AI Developer to join their team.
    Austin Richardson
    336-413-9794 | arichardson@pipercompanies.com
    """
    extractor = EmailExtractor(sample_text)
    print(extractor.extract_email_info_from_jd(sample_text))

