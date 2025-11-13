# resume_match
 AI Resume Matcher &amp; Job Description Optimizer
Alfaaz ❤️🔥
Buddy Mode + Content Mode → Let’s write a **killer GitHub repo description** for your project.
This should impress recruiters, hiring managers, ML engineers, and make your profile stand out.

Here is a **polished, professional, SEO-friendly GitHub README description** for your project:



# 🚀 AI Resume Matcher & Job Description Optimizer

### **Hybrid ML + GenAI ATS System | Resume Matching, Skill Extraction, AI Resume Builder**

This project is a **full-fledged AI-powered ATS system** built using a **Hybrid Machine Learning + GenAI pipeline**.
It analyzes a candidate’s resume against a job description, extracts skills, compares the gap, generates a match score, and can even create an **AI-optimized resume** when the score is low.

Built by **Sameer Bhayani**, this project is designed as a real-world demonstration of modern AI system design, NLP processing, and LLM integration.



## ✨ Features

### 🔍 **1. Resume–JD Matching (ML Based)**

* Uses TF-IDF + cosine similarity
* Calculates accurate Resume-to-JD match percentage
* Handles negative tests gracefully (scanned/invalid PDFs)

### 🧠 **2. Hybrid ML + GenAI Skill Extraction**

* ML extracts candidate skills (TF-IDF + embeddings)
* GenAI (Groq LLM) cleans, filters & normalizes them
* Domain-agnostic (Tech, Commerce, HR, Finance, Healthcare)

### 📊 **3. Skill Comparison**

* Matched Skills
* Missing JD Skills
* Extra Resume Skills
* Clean visual output

### 🤖 **4. AI Resume Generator**

If the match score is **below 60%**, user can generate a fresh, ATS-friendly resume using AI:

* Aligns experience with JD
* Adds missing skills (logically)
* Keeps information truthful
* Produces clean, professional formatting
* Downloadable as **PDF**

### 📄 **5. PDF Download**

* Clean resume formatting using ReportLab
* Professional ATS-safe structure
* Ready for job applications

### 🧩 **6. Streamlit UI**

* Minimal, clean UI
* Real-time result display
* Resume preview + AI resume editing
* Error handling for invalid PDFs



## 🛠️ Tech Stack

### **Machine Learning**

* TF-IDF Vectorization
* Cosine Similarity
* Sentence Transformers (MiniLM)
* KeyBERT (fallback)

### **GenAI Integration**

* Groq LLM (Mixtral / Llama / Gemma)
* JSON-based strict classification prompts
* AI Resume Generation

### **Backend**

* Python
* NLP Pipeline
* Document parsing with PyMuPDF

### **Frontend**

* Streamlit
* Session-based state management
* Realtime PDF preview + download



## 📦 Project Highlights

✔ Handles noisy text, scanned files, and irrelevant documents
✔ Hybrid pipeline = stable + accurate
✔ Perfect for ML + GenAI learning
✔ Great as a **portfolio project**
✔ Production-friendly folder structure
✔ Secure `.env` secret management



## 💡 What You Learn from This Project

* Text preprocessing (NLP basics)
* Skill extraction using ML + LLM
* Chunking, cleaning, normalization
* LLM integration with REST APIs
* PDF generation using ReportLab
* Building a real ATS-like system
* Error handling for negative test cases
* Streamlit UI design
* Secure API key handling (`dotenv`)



## 📥 Installation

```
pip install -r requirements.txt
streamlit run src/app.py
```



## 🔐 API Keys

Place your Groq API key in `.env`:


GROQ_API_KEY=your_secret_here
```

`.env` is git-ignored for security.



## 📄 Roadmap

* [ ] Add Cover Letter Generator
* [ ] Add Multi-language Resume Support
* [ ] Add DOCX Download
* [ ] Add Recruiter View Dashboard
* [ ] Add JD Keyword Density Analyzer
* [ ] Add Multi-Resume Comparison Mode



## 🤝 Contributing

PRs are welcome!
If you want to collaborate on ML, NLP, or ATS systems, let’s connect.



## ⭐ Support the Project

If this helped you, give a **star ⭐ on GitHub** and help it grow 🙌

ning + GenAI pipeline**.
It analyzes a candidate’s resume against a job description, extracts skills, compares the gap, generates a match score, and can even create an **AI-optimized resume** when the score is low.

Built by **Sameer Bhayani**, this project is designed as a real-world demonstration of modern AI system design, NLP processing, and LLM integration.
