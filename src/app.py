# src/app.py
import streamlit as st
from extract_text import extract_text   # your PDF text extractor
from match import match_resume_job, compare_skills_hybrid
from resume_generator import generate_resume_with_ai
from pdf_generator import generate_resume_pdf

st.set_page_config(page_title="AI Resume Matcher", layout="wide")
st.title("AI Resume Matcher — Sameer Bhayani")
st.write("Upload Resume and Job Description (PDF) — hybrid ML extracts candidates; GenAI filters skills.")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
with col2:
    jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

domain_hint = st.text_input("Optional: domain hint (e.g., commerce, healthcare, tech)", "")

if st.button("Analyze"):
    if not resume_file or not jd_file:
        st.warning("Upload both files")
    else:
        with st.spinner("Extracting text..."):
            rpath = resume_file
            jpath = jd_file
            # if your import_file returns a temp path use that; here we assume file-like object accepted by extract_text
            resume_text = extract_text(rpath)
            jd_text = extract_text(jpath)
        score = match_resume_job(resume_text, jd_text)
        st.session_state.score = score
        st.session_state.resume_text = resume_text
        st.session_state.jd_text  =  jd_text
        missing, extra, matched, filtered = compare_skills_hybrid(resume_text, jd_text, domain_hint)
        st.session_state.missing = missing
        st.metric("Match Score", f"{score*100:.2f}%")
        st.subheader("Matched Skills")
        st.write(matched or "No matched skills detected")
        st.subheader("Missing Skills (from JD)")
        st.write(missing or "No missing skills detected")
        st.subheader("Extra Skills (from Resume)")
        st.write(extra or "No extra skills detected")
        st.subheader("Filtered candidates (raw)")
        st.write(filtered or [])

score = st.session_state.get("score") or 1
resume_text = st.session_state.get("resume_text")
jd_text = st.session_state.get("jd_text")
missing = st.session_state.get("missing")
if  score < 0.60:
    if st.button("Create Matching Resume with AI"):
        optimized_resume = generate_resume_with_ai(resume_text, jd_text, missing)
        st.subheader("AI-Generated Matching Resume")
        st.text_area("Resume Preview", optimized_resume, height=400)
        pdf_file = generate_resume_pdf(optimized_resume)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="Download Resume as PDF",
                data=f,
                file_name="optimized_resume.pdf",
                mime="application/pdf"
            )