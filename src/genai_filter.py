import os
import requests
import json
import re
from typing import List
from dotenv import load_dotenv
import streamlit as st

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def prompt_for_skill_filter(candidates: List[str], domain_hint: str = "") -> str:
    domain_hint_text = f" Domain: {domain_hint}." if domain_hint else ""
    return f"""
    You are an AI model trained to extract ONLY professional skills, tools, technologies, and software names.
    STRICT RULES:
    - RETURN JSON LIST ONLY.
    - REMOVE job titles like 'software engineer', 'developer', 'manager'.
    - REMOVE generic words like 'tech', 'services', 'experience', 'skills'.
    - REMOVE responsibilities (e.g., 'manage team', 'build microservices').
    - KEEP ONLY actual skills such as programming languages, frameworks, tools, cloud platforms, commerce tools.
    {domain_hint_text}
    Candidates: {candidates}
    Return JSON array only.
    """


def call_groq_filter(candidates: List[str], domain_hint: str = "") -> List[str]:
    if not GROQ_API_KEY:
        raise EnvironmentError("GROQ_API_KEY not set in environment")

    prompt = prompt_for_skill_filter(candidates, domain_hint)

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 512
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    resp = requests.post(GROQ_URL, json=payload, headers=headers, timeout=20)
    
    resp.raise_for_status()
    out = resp.json()

    text = out["choices"][0]["message"]["content"]

    try:
        skills = json.loads(text)
        return [s.lower().strip() for s in skills]
    except:
        cleaned = re.sub(r'[\[\]]', '', text)
        parts = [p.strip('", ').lower() for p in re.split(r'[\n,]+', cleaned)]
        return [p for p in parts if p]
