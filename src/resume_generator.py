import os
from dotenv import load_dotenv
import requests
import streamlit as st


load_dotenv();
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_resume_with_ai(original_resume, job_description, missing_skills):
    #st.write(GROQ_API_KEY);
  
    prompt = f"""
You are an expert resume writer.

Rewrite the candidate's resume to better match the job description.

RULES:
- DO NOT fabricate fake companies or fake degrees.
- YOU MAY rewrite responsibilities using JD keywords.
- YOU MAY strengthen skills using the missing skills list if they logically apply.
- Make the resume ATS-friendly.
- Use clean formatting.
- Add a professional summary aligned with the JD.
- Maintain honesty but optimize wording.

Candidate Resume:
{original_resume}

Job Description:
{job_description}

Missing Skills:
{missing_skills}

Return only the updated resume in plain text.
"""

    response = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 1200,
        },
    )
    return response.json()["choices"][0]["message"]["content"]
