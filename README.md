# JobFit AI – Smart Resume-to-Job Matcher

🎯 A next-gen ATS assistant that helps job seekers beat the resume screening process using **AI-powered parsing and matching**.

No more guessing — JobFit AI tells you:
- ✅ Which skills to highlight
- ⚠️ What’s missing from your resume
- 💡 How to rephrase bullets for ATS
- 📊 Your real match score

Powered by **Google Gemini** and modern NLP.

---

## 🚀 Features

| Feature | Description |
|-------|-------------|
| 📄 **Resume Parsing** | Extracts skills, experience, education from PDF |
| 📋 **Job Description Analysis** | Parses requirements using LLMs |
| 🔍 **Smart Matching** | Compares resume vs job using semantic understanding |
| 💬 **AI Suggestions** | Generates ATS-friendly bullet points to add |
| 🌐 **Web UI** | Streamlit frontend + FastAPI backend |
| 🐳 **Docker Ready** | Containerized for easy deployment |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI
- **LLM**: Google Gemini 1.5 Flash
- **Parsing**: `pdfplumber`, `google-generativeai`
- **DevOps**: Docker, GitHub Actions
- **Database**: SQLite (MVP), PostgreSQL (future)

---

## 🚀 Quick Start

### 1. Set up environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
