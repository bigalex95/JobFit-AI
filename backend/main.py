import sys
import os

# Add the current directory (backend/) to sys.path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

# Now these will work:
from utils.pdf_parser import extract_text_from_pdf
from utils.jd_parser import parse_job_description
from utils.matcher import calculate_skill_match, estimate_experience
from utils.ai_suggestions import generate_resume_suggestions

app = FastAPI(title="JobFit AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse-jd")
async def parse_jd(text: Annotated[str, Form()]):
    result = parse_job_description(text)
    return result


@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    filepath = f"data/resumes/{file.filename}"
    os.makedirs("data/resumes", exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(filepath)
    return {"text": text[:1000], "full_text": text}


@app.post("/match")
async def match(jd_text: Annotated[str, Form()], resume_file: UploadFile = File(...)):
    # Parse JD
    jd_data = parse_job_description(jd_text)

    # Save and parse resume
    os.makedirs("data/resumes", exist_ok=True)
    resume_path = f"data/resumes/{resume_file.filename}"
    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())

    resume_text = extract_text_from_pdf(resume_path)

    # Match skills
    skill_match = calculate_skill_match(resume_text, jd_data["skills_required"])
    exp_match = estimate_experience(resume_text, jd_data["experience_required"])

    # Generate AI Suggestions
    ai_suggestions = generate_resume_suggestions(
        jd_text=jd_text,
        resume_text=resume_text,
        missing_skills=skill_match["missing_skills"],
        experience_gap=exp_match,
    )

    return {
        "job_summary": jd_data,
        "skill_match": skill_match,
        "experience_match": exp_match,
        "ai_suggestions": ai_suggestions,
        "overall_score": (
            skill_match["match_percentage"]
            + (50 if exp_match["meets_requirement"] else 0)
        )
        // 2,
    }
