# src/match.py
from processor import extract_candidates_and_selected, clean_text
from genai_filter import call_groq_filter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Toggle whether to use GenAI filter (if False, uses selected from processor.py)
USE_GENAI = True

def match_resume_job(resume_text: str, jd_text: str) -> float:
    r = clean_text(resume_text)
    j = clean_text(jd_text)

    # NEGATIVE TEST HANDLING
    if not r or not j:
        return 0.0   # treat as no match

    try:
        vec = TfidfVectorizer(stop_words="english")
        tf = vec.fit_transform([r, j])
        return float(cosine_similarity(tf[0:1], tf[1:2])[0][0])
    except ValueError:
        return 0.0
    vec = TfidfVectorizer(stop_words="english")
    tf = vec.fit_transform([clean_text(resume_text), clean_text(jd_text)])
    return float(cosine_similarity(tf[0:1], tf[1:2])[0][0])

def compare_skills_hybrid(resume_text: str, jd_text: str, domain_hint: str = ""):
    candidates, selected_ml = extract_candidates_and_selected(resume_text, jd_text)
    print("ML candidates:", selected_ml)
    if USE_GENAI:
        try:
            # Ask LLM to filter + canonicalize skills from the ML candidates
            filtered = call_groq_filter(selected_ml or candidates, domain_hint)
            print("GenAI filtered:", filtered)
   
            # Build sets by checking which filtered items appear in resume/jd cleaned text
            cleaned_resume = clean_text(resume_text)
            cleaned_jd = clean_text(jd_text)
            resume_set = set([s for s in filtered if s in cleaned_resume or s.replace(" ", "") in cleaned_resume])
            jd_set = set([s for s in filtered if s in cleaned_jd or s.replace(" ", "") in cleaned_jd])
            # Also include if candidate semantically matches doc (embedding-based check could be added)
            # final sets:
            matched = sorted(list(resume_set & jd_set))
            missing = sorted(list(jd_set - resume_set))
            extra   = sorted(list(resume_set - jd_set))
            return missing, extra, matched, filtered
        except Exception as e:
            # fallback to ML-only selected list
            pass
    # ML-only fallback
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)
    resume_set = set([s for s in selected_ml if s in cleaned_resume or s.replace(" ", "") in cleaned_resume])
    jd_set = set([s for s in selected_ml if s in cleaned_jd or s.replace(" ", "") in cleaned_jd])
    matched = sorted(list(resume_set & jd_set))
    missing = sorted(list(jd_set - resume_set))
    extra   = sorted(list(resume_set - jd_set))
    return missing, extra, matched, selected_ml
