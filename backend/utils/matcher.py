# backend/utils/matcher.py

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import torch
import re

# Load model once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_skill_match(resume_text: str, required_skills: list) -> dict:
    if not required_skills:
        return {"matched_skills": [], "missing_skills": [], "match_percentage": 0}

    # Encode
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    skill_embeddings = model.encode(required_skills, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = cos_sim(resume_embedding, skill_embeddings)[
        0
    ]  # [0] to remove batch dim
    similarities = similarities.cpu().numpy()  # Convert to NumPy

    matched_skills = []
    missing_skills = []

    for skill, score in zip(required_skills, similarities):
        if score > 0.4:  # Lower threshold for better recall
            matched_skills.append(
                {"skill": skill, "match_score": round(float(score), 2)}
            )
        else:
            missing_skills.append(
                {"skill": skill, "match_score": round(float(score), 2)}
            )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": (
            min(100, int((len(matched_skills) / len(required_skills)) * 100))
            if required_skills
            else 0
        ),
    }


def estimate_experience(resume_text: str, required: str) -> dict:
    # Broader pattern to catch "10+ years", "over 5 years", "more than 3 years", etc.
    resume_matches = re.findall(
        r"(\d+)\+?\s*(?:\+)?\s*years?\s*(?:of)?(?:\s+(?:experience|software|ai|ml|development|work))?",
        resume_text,
        re.IGNORECASE,
    )

    resume_years = "Not found"
    max_resume_years = 0
    if resume_matches:
        max_resume_years = max(map(int, resume_matches))
        resume_years = f"{max_resume_years} years"

    # Extract required
    req_match = re.search(r"(\d+)\+?\s*years?", required, re.IGNORECASE)
    required_years = int(req_match.group(1)) if req_match else 0

    meets = max_resume_years >= required_years if required_years > 0 else False

    return {
        "resume_years": resume_years,
        "required_years": required_years,
        "meets_requirement": meets,
    }
