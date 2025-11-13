from extract_text import extract_text
from match import compare_skills_hybrid, match_resume_job

r = extract_text("sample_resume.pdf")
j = extract_text("sample_job_description.pdf")
missing, extra, matched, filtered = compare_skills_hybrid(r, j, domain_hint="tech")
print("Matched:", matched)
print("Missing:", missing)
print("Extra:", extra)
print("FilteredCandidates:", filtered)
print("MatchScore:", match_resume_job(r,j))
