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

| Feature                         | Description                                         |
| ------------------------------- | --------------------------------------------------- |
| 📄 **Resume Parsing**           | Extracts skills, experience, education from PDF     |
| 📋 **Job Description Analysis** | Parses requirements using LLMs                      |
| 🔍 **Smart Matching**           | Compares resume vs job using semantic understanding |
| 💬 **AI Suggestions**           | Generates ATS-friendly bullet points to add         |
| 🌐 **Web UI**                   | Streamlit frontend + FastAPI backend                |
| 🐳 **Docker Ready**             | Containerized for easy deployment                   |

### 🔤 AI Bullet Rewriter

- Paste any bullet from your resume
- Get an ATS-optimized, keyword-rich version
- Powered by Gemini 2.5 Flash
- Context-aware: uses job description and your resume

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI
- **LLM**: Google Gemini 2.5 Flash
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
```

### 2. Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create API key
3. Export it:

```bash
export GEMINI_API_KEY="your_key_here"
```

### 3. Run Backend

```bash
uvicorn backend.main:app --reload --port=8000
```

### 4. Run Frontend

```bash
streamlit run frontend/app.py
```

👉 Open http://localhost:8501

---

## 🧪 Example Use Case

**Job**: Senior ML Scientist (5+ years, PyTorch, NLP, MLOps)  
**Resume**: Alibek Erkabayev (10+ years, Python, TensorFlow, AWS)  
**Output**:

- Match Score: 70%
- Feedback: "Add fine-tuning (LoRA, QLoRA), anomaly detection"
- Suggestions: "Fine-tuned LLMs using LoRA for efficient deployment..."

---

## 🌐 Roadmap

| Feature                     | Status  |
| --------------------------- | ------- |
| ✅ LLM-powered parsing      | Done    |
| 🔤 AI Bullet Rewriter       | Done    |
| 📤 Export Optimized Resume  | Planned |
| 🧩 Chrome Extension         | Planned |
| ☁️ Deploy to Railway/Render | Future  |

---

## 🤝 Contributing

PRs welcome! Just:

1. Create a feature branch
2. Add tests if possible
3. Submit PR to `main`

---

## 📄 License

MIT
