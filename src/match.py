# match.py
from sentence_transformers import SentenceTransformer, util
from processor import clean_text, extract_candidates_and_selected
import re
import numpy as np

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def extract_years(text):
    match = re.search(r'(\d+)\+?\s*years', text.lower())
    return int(match.group(1)) if match else 0

def embed_skills(skills):
    """Embed list of skills into vectors."""
    if not skills:
        return None
    return embedder.encode(skills, convert_to_tensor=True)

def skill_semantic_similarity(resume_skills, jd_skills):
    """Average similarity between resume skills and JD skills."""
    if not resume_skills or not jd_skills:
        return 0.0
    
    emb_resume = embed_skills(resume_skills)
    emb_jd = embed_skills(jd_skills)

    sim_matrix = util.cos_sim(emb_resume, emb_jd)
    return float(sim_matrix.mean())

def smart_ats_score_v2(resume_text, jd_text, matched, missing, filtered_skills):
    # -------------------------
    # 1. SKILL MATCH RATIO (50%)
    # -------------------------
    total_jd_skills = len(filtered_skills)
    if total_jd_skills == 0:
        skill_match_ratio = 0
    else:
        skill_match_ratio = len(matched) / total_jd_skills

    # -------------------------
    # 2. SKILL SEMANTIC SIMILARITY (35%)
    # -------------------------
    semantic_skill_score = skill_semantic_similarity(
        resume_skills=matched + list(set(filtered_skills) - set(missing)),
        jd_skills=filtered_skills
    )

    # -------------------------
    # 3. EXPERIENCE ALIGNMENT (10%)
    # -------------------------
    resume_exp = extract_years(resume_text)
    jd_exp = extract_years(jd_text)

    exp_score = 1 if resume_exp >= jd_exp else 0

    # -------------------------
    # 4. KEYWORD OVERLAP (5%)
    # -------------------------
    resume_words = set(clean_text(resume_text).split())
    jd_words = set(clean_text(jd_text).split())
    keyword_overlap = len(resume_words & jd_words) / (len(jd_words) + 1)

    # -------------------------
    # FINAL SCORE
    # -------------------------
    final = (
        skill_match_ratio * 0.50 +
        semantic_skill_score * 0.35 +
        exp_score * 0.10 +
        keyword_overlap * 0.05
    )

    return max(0, min(final, 1))  # normalize between 0-1

def compare_skills_hybrid(resume_text: str, jd_text: str, domain_hint: str = ""):
    candidates, selected_ml = extract_candidates_and_selected(resume_text, jd_text)
    #print("ML candidates:", selected_ml)
    USE_GENAI = True
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