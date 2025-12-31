#!/usr/bin/env python3
"""
Script to create a resume using the ResumeOptimizer class

Usage:
    python create_resume.py
    
    Or pass a job description as argument:
    python create_resume.py "your job description here"
"""

import sys
from llm_exctration import ResumeOptimizer


def main():
    """Main function to create resume"""
    
    # Sample job description - you can modify this or pass it as argument
    if len(sys.argv) > 1:
        # Use job description from command line argument
        job_description = ' '.join(sys.argv[1:])
    else:
        # Default job description
        job_description = """
        Position: Data Engineer AI/ML Pipelines
        Location: Seffner FL (Hybrid)
        Duration: 12+ months Contract
        Visa: USC & GC only
        
        Job Description:
        They will also interview strong developers that have exposure to, experience with, or a good knowledge of Data Engineering.
        They will be doing a hybrid role of writing some code and setting up pipelines.
        
        General Requirements:
        - Develop backend services and APIs for WMS
        - Build ETL/ELT pipelines using Azure Data Factory & Databricks
        - Implement CI/CD, instrumentation, and observability
        - Prepare datasets for AI/ML and predictive analytics
        - Ensure data quality through validation, anomaly detection, and lineage tracking
        - Python, C#/.NET, Java for app development
        - Advanced SQL and distributed data systems
        - Cloud platforms (Azure), Databricks, orchestration tools
        - API design and microservices
        - Partner with data scientists, BI developers, and platform engineers
        
        Required Qualifications:
        - Bachelors in CS or related field (preferred)
        - 5+ years in software development/data engineering
        - Proficiency in Python, SQL, and C#
        - Familiarity with WMS/logistics systems
        - Certifications in Azure/Data Engineering (preferred)
        
        Key Responsibilities:
        - Build and maintain data pipelines optimized for machine learning workflows
        - Partner with data scientists to prepare feature sets
        - Implement data versioning and support model retraining and evaluation
        - Ingest and transform structured/unstructured data from WMS
        - Design and automate scalable, modular pipelines using Azure Data Factory
        - Implement anomaly detection and data reconciliation
        - Contribute to metadata management, data lineage, and auditable transformations
        """
    
    print("=" * 80)
    print("RESUME OPTIMIZER - Creating Resume")
    print("=" * 80)
    print(f"\nJob Description: {job_description[:200]}...")
    print("\nStarting resume creation process...")
    print("=" * 80)
    
    try:
        # Create ResumeOptimizer instance with job description
        optimizer = ResumeOptimizer(job_description)
        
        # Execute the complete workflow
        print("\nStep 1: Extracting skills from job description...")
        print("Step 2: Generating optimized resume JSON...")
        print("Step 3: Creating resume document...")
        print()
        
        resume_path = optimizer.workflow()
        
        if resume_path:
            print("=" * 80)
            print("✓ SUCCESS!")
            print(f"✓ Resume created successfully at: {resume_path}")
            print("=" * 80)
            return 0
        else:
            print("=" * 80)
            print("✗ FAILED!")
            print("Could not create resume. Please check the logs above for errors.")
            print("=" * 80)
            return 1
            
    except Exception as e:
        print("=" * 80)
        print("✗ ERROR!")
        print(f"An error occurred: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

