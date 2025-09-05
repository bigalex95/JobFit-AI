from typing import List
import pdfplumber

# backend/utils/jd_parser.py

import re

# Case-insensitive, flexible matching
SKILL_PATTERNS = {
    "Python": r"python",
    "TensorFlow": r"tensor\s*flow|tf",
    "PyTorch": r"py\s*torch|torch",
    "AWS": r"aws|amazon\s*web\s*services",
    "Azure": r"azure|azure\s*cloud",
    "GCP": r"gcp|google\s*cloud",
    "NLP": r"nlp|natural\s*language|langchain|llm|large\s*language\s*model",
    "MLOps": r"mlops|ci/cd|docker|kubernetes|model\s*deployment",
    "SQL": r"sql|structured\s-?query\s-?language",
    "Machine Learning": r"machine\s*learning|ml|ai",
    "Deep Learning": r"deep\s*learning|neural\s*network|cnn|gan",
    "PyTorch": r"py\s*torch|torch",
    "Computer Vision": r"computer\s*vision|cv|opencv|object\s*detection|slam",
    "Fine-tuning": r"fine\s*tuning|lora|qlora|sft|adapter",
    "Recommendation System": r"recommendation|recommender|personalization",
    "Anomaly Detection": r"anomaly\s*detection|outlier\s*detection",
}


def extract_skills(text: str) -> List[str]:
    text_lower = re.sub(r"\s+", " ", text.lower().replace("\n", " "))  # Normalize
    found_skills = []
    for skill, pattern in SKILL_PATTERNS.items():
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    return list(set(found_skills))


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()
