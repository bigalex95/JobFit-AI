import re
import spacy
from typing import Dict, List

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Common skill patterns (extendable)
SKILL_KEYWORDS = [
    "python",
    "tensorflow",
    "pytorch",
    "aws",
    "docker",
    "kubernetes",
    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",
    "sql",
    "git",
    "flask",
    "django",
    "api",
    "rest",
    "mlops",
]


def extract_experience(text: str) -> str:
    patterns = [
        r"(\d+)\+?\s*years?\s+of\s+experience",
        r"experience:\s*(\d+)",
        r"minimum\s+(\d+)\s+years?",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)} years"
    return "Not specified"


def extract_skills(text: str) -> List[str]:
    doc = nlp(text.lower())
    found_skills = []

    # Exact keyword matching (can be improved later with NER or embeddings)
    for skill in SKILL_KEYWORDS:
        if skill in doc.text:
            found_skills.append(skill.title())

    # Remove duplicates
    return list(set(found_skills))


def parse_job_description(text: str) -> Dict:
    return {
        "experience_required": extract_experience(text),
        "skills_required": extract_skills(text),
        "raw_text_length": len(text),
    }


if __name__ == "__main__":
    sample_jd = """
    We are looking for a Machine Learning Engineer with 3+ years of experience.
    Must have skills in Python, TensorFlow, AWS, and Docker.
    Knowledge of MLOps and model deployment is a plus.
    """
    print(parse_job_description(sample_jd))
