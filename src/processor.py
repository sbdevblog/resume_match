# src/processor.py
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT

nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))

EMBED_MODEL = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBED_MODEL)
keybert_model = KeyBERT(model=EMBED_MODEL)

def clean_text(text: str) -> str:
    if not text:
        return ""
    t = text.lower()
    t = re.sub(r'\S+@\S+', ' ', t)            # remove emails
    t = re.sub(r'\+?\d[\d\-\s()]{5,}', ' ', t) # remove phone-ish
    t = re.sub(r'http\S+', ' ', t)
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    tokens = [tok for tok in t.split() if len(tok) > 1 and tok not in stop_words]
    return " ".join(tokens)

def candidates_from_doc(text: str, top_k=80):
    cleaned = clean_text(text)
    if not cleaned:
        return []
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=top_k)
    vec.fit([cleaned])
    return list(vec.get_feature_names_out())

def top_tokens(text: str, n=60):
    cleaned = clean_text(text)
    if not cleaned:
        return []
    cnt = Counter(cleaned.split())
    return [w for w, _ in cnt.most_common(n)]

def joint_candidates(resume_text: str, jd_text: str, top_k_each=100):
    cand_r = candidates_from_doc(resume_text, top_k=top_k_each)
    cand_j = candidates_from_doc(jd_text, top_k=top_k_each)
    tok_r = top_tokens(resume_text, n=80)
    tok_j = top_tokens(jd_text, n=80)
    # union with order preserved
    seen = set()
    out = []
    for item in (cand_r + cand_j + tok_r + tok_j):
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out

# lightweight semantic filter (no anchor list)
def semantic_select(candidates, resume_text, jd_text, sim_threshold=0.36):
    if not candidates:
        return []
    cand_emb = embedder.encode(candidates, convert_to_tensor=True, show_progress_bar=False)
    res_vec = embedder.encode(clean_text(resume_text), convert_to_tensor=True, show_progress_bar=False)
    jd_vec  = embedder.encode(clean_text(jd_text), convert_to_tensor=True, show_progress_bar=False)
    sim_res = util.cos_sim(cand_emb, res_vec).cpu().numpy().reshape(-1)
    sim_jd  = util.cos_sim(cand_emb, jd_vec).cpu().numpy().reshape(-1)
    selected = []
    for i, cand in enumerate(candidates):
        r = float(sim_res[i]); j = float(sim_jd[i])
        if max(r, j) >= sim_threshold or (r + j)/2 >= (sim_threshold - 0.05):
            selected.append(cand)
    # filter obvious noise
    generic_blacklist = {"company","apply","job","role","location","email","phone","resume","cv","linkedin",
                         "apply now","careers","responsibilities","requirements","engineer", "software engineer", "developer", "manager", "lead", "architect"}
   
    final = [c for c in set(selected) if not any(b in c for b in generic_blacklist)]
    return final

# fallback: KeyBERT extraction (useful if LLM unavailable or to get richer ngrams)
def keybert_candidates(text: str, top_n=20):
    cleaned = clean_text(text)
    if not cleaned:
        return []
    kws = keybert_model.extract_keywords(cleaned, keyphrase_ngram_range=(1,2), stop_words="english", top_n=top_n)
    return [kw for kw, _ in kws]

# top-level helper: returns candidate list & filtered skill-like candidates
def extract_candidates_and_selected(resume_text: str, jd_text: str, top_k_each=100, sim_threshold=0.36):
    candidates = joint_candidates(resume_text, jd_text, top_k_each=top_k_each)
    selected = semantic_select(candidates, resume_text, jd_text, sim_threshold=sim_threshold)
    # if selected is empty or too small, augment with KeyBERT candidates
    if len(selected) < 4:
        kb = keybert_candidates(resume_text + " " + jd_text, top_n=30)
        # merge and re-run semantic select
        combined = list(dict.fromkeys(candidates + kb))
        selected = semantic_select(combined, resume_text, jd_text, sim_threshold=sim_threshold-0.03)
    return candidates, selected
