import requests
from bs4 import BeautifulSoup
import re
import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
import logging

load_dotenv()

class JobScraper:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            logging.error("❌ GROQ_API_KEY not found in environment variables")
            self.groq_model = None
        else:
            try:
                self.groq_model = ChatGroq(
                    groq_api_key=self.groq_api_key,
                    model_name="llama-3.3-70b-versatile"
                )
                logging.info("✅ Groq model initialized successfully")
            except Exception as e:
                logging.error(f"❌ Failed to initialize Groq model: {e}")
                self.groq_model = None
    
    def scrape_nvoids(self, url, keywords=None):
        """Scrape job listings from NVoids website"""
        try:
            logging.info(f"Scraping URL: {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all job listings (adjust selectors based on actual website structure)
            job_elements = soup.find_all(['div', 'article', 'section'], class_=re.compile('job|listing|post', re.I))
            
            if not job_elements:
                # Try alternative selectors
                job_elements = soup.find_all('tr', class_=re.compile('job', re.I))
            
            if not job_elements:
                job_elements = soup.find_all('div', id=re.compile('job', re.I))
            
            jobs = []
            
            for element in job_elements:
                try:
                    job_data = self._extract_job_info(element)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logging.error(f"Error extracting job info: {e}")
                    continue
            
            # Filter by keywords if provided
            if keywords and jobs:
                keywords_lower = [k.strip().lower() for k in keywords.split(',')]
                filtered_jobs = []
                for job in jobs:
                    job_text = ' '.join([
                        job.get('title', ''),
                        job.get('jd', ''),
                        job.get('company', '')
                    ]).lower()
                    
                    if any(keyword in job_text for keyword in keywords_lower):
                        filtered_jobs.append(job)
                
                jobs = filtered_jobs
            
            # Use LLM to parse and enhance job data
            if self.groq_model and jobs:
                enhanced_jobs = self._enhance_with_llm(jobs)
                return enhanced_jobs
            
            return jobs
            
        except Exception as e:
            logging.error(f"Error scraping website: {e}")
            return []
    
    def _extract_job_info(self, element):
        """Extract basic job information from HTML element"""
        job_data = {}
        
        # Try to find title
        title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=re.compile('title|job-title', re.I))
        if not title_elem:
            title_elem = element.find('a', href=True)
        
        if title_elem:
            job_data['title'] = title_elem.get_text(strip=True)
        
        # Try to find company
        company_elem = element.find(['span', 'div'], class_=re.compile('company', re.I))
        if company_elem:
            job_data['company'] = company_elem.get_text(strip=True)
        
        # Try to find location
        location_elem = element.find(['span', 'div'], class_=re.compile('location', re.I))
        if location_elem:
            job_data['location'] = location_elem.get_text(strip=True)
        
        # Get all text content
        full_text = element.get_text(separator=' ', strip=True)
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, full_text)
        if emails:
            job_data['email'] = emails[0]
        
        # Extract phone
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{3}-\d{3}-\d{4}',
            r'\(\d{3}\)\s?\d{3}-\d{4}'
        ]
        for pattern in phone_patterns:
            phones = re.findall(pattern, full_text)
            if phones:
                job_data['phone'] = phones[0]
                break
        
        # Store full text as JD
        job_data['jd'] = full_text
        
        return job_data if job_data else None
    
    def _enhance_with_llm(self, jobs):
        """Use LLM to parse and enhance job data"""
        try:
            enhanced_jobs = []
            
            for job in jobs:
                job_text = job.get('jd', '')
                
                system_prompt = """You are an expert job data parser. Extract structured information from job listings.
                Return ONLY valid JSON with these exact fields:
                {
                    "title": "Job title",
                    "company": "Company name",
                    "location": "Location",
                    "recruiter_name": "Recruiter name",
                    "phone": "Phone number",
                    "email": "Email address",
                    "visa_type": "Required visa (e.g., H1B, GC, USC, EAD, etc.) or null",
                    "jd": "Full job description",
                    "requirements": "Key requirements summary"
                }
                
                Important rules:
                - Extract visa requirements if mentioned
                - Extract recruiter contact information
                - Keep the full job description in 'jd' field
                - Return ONLY JSON, no other text"""
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=f"Parse this job listing:\n\n{job_text}")
                ]
                
                try:
                    response = self.groq_model.invoke(messages)
                    response_text = response.content.strip()
                    
                    # Extract JSON from response
                    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                    if json_match:
                        parsed_job = json.loads(json_match.group(0))
                        enhanced_jobs.append(parsed_job)
                    else:
                        # Fallback to original data
                        enhanced_jobs.append(job)
                        
                except Exception as e:
                    logging.error(f"LLM parsing error: {e}")
                    enhanced_jobs.append(job)
            
            return enhanced_jobs
            
        except Exception as e:
            logging.error(f"Error enhancing with LLM: {e}")
            return jobs

if __name__ == "__main__":
    scraper = JobScraper()
    jobs = scraper.scrape_nvoids("https://nvoids.com/search_sph.jsp")
    print(f"Found {len(jobs)} jobs")
    for job in jobs:
        print(json.dumps(job, indent=2))

