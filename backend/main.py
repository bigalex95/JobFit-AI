import sys
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import json

# Add backend/ to path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import LLM-based modules
from utils.pdf_parser import extract_text_from_pdf
from utils.llm_resume_parser import parse_resume_with_llm
from utils.llm_jd_parser import parse_jd_with_llm
from utils.llm_matcher import run_llm_match
from utils.bullet_rewriter import rewrite_bullet_point

# Initialize FastAPI
app = FastAPI(title="JobFit AI - LLM Enhanced Backend")

# Allow frontend (Streamlit) to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure data/resumes exists
os.makedirs("data/resumes", exist_ok=True)


@app.post("/parse-resume")
async def api_parse_resume(file: UploadFile = File(...)):
    filepath = f"data/resumes/{file.filename}"
    with open(filepath, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(filepath)
    return {"text": text[:1000], "full_text": text}


@app.post("/parse-jd")
async def api_parse_jd(text: Annotated[str, Form()]):
    return {"raw_text": text}


@app.post("/match")
async def match(jd_text: Annotated[str, Form()], resume_file: UploadFile = File(...)):
    # --- 1. Save & Extract Resume Text ---
    resume_path = f"data/resumes/{resume_file.filename}"
    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())

    resume_text = extract_text_from_pdf(resume_path)

    # --- 2. Parse Resume with LLM ---
    parsed_resume = parse_resume_with_llm(resume_text)
    if not parsed_resume["success"]:
        return {
            "error": "Failed to parse resume with LLM",
            "details": parsed_resume["error"],
            "raw_output": parsed_resume.get("raw_output", ""),
        }

    # --- 3. Parse Job Description with LLM ---
    parsed_jd = parse_jd_with_llm(jd_text)
    if not parsed_jd["success"]:
        return {
            "error": "Failed to parse job description with LLM",
            "details": parsed_jd["error"],
            "raw_output": parsed_jd.get("raw_output", ""),
        }

    # --- 4. Run Semantic Match with LLM ---
    match_result = run_llm_match(parsed_resume["data"], parsed_jd["data"])
    if not match_result["success"]:
        return {
            "error": "Failed to generate match feedback",
            "details": match_result["error"],
        }

    # --- 5. Estimate Match Score (Simple Heuristic) ---
    # You can improve this later with more logic
    required_skills_count = (
        len(parsed_jd["data"].get("required_skills", {}).get("ml_frameworks", []))
        + len(parsed_jd["data"].get("required_skills", {}).get("languages", []))
        + len(parsed_jd["data"].get("required_skills", {}).get("cloud", []))
    )

    # Very basic: if feedback says "missing", count them
    missing_count = (
        match_result["feedback"].lower().count("missing")
        if "missing" in match_result["feedback"].lower()
        else 0
    )
    match_percentage = max(0, 100 - (missing_count * 10))  # rough estimate

    if parsed_resume["data"]["years_of_experience"] < parsed_jd["data"].get(
        "required_years", 0
    ):
        match_percentage = max(0, match_percentage - 20)

    # --- 6. Return Structured Response ---
    return {
        "job_summary": {
            "job_title": parsed_jd["data"].get("job_title"),
            "required_years": parsed_jd["data"].get("required_years"),
            "required_education": parsed_jd["data"].get("required_education"),
            "required_skills": parsed_jd["data"].get("required_skills"),
        },
        "parsed_resume": parsed_resume["data"],
        "ai_feedback": match_result["feedback"],
        "overall_score": match_percentage,
    }


@app.post("/rewrite-bullet")
async def api_rewrite_bullet(
    bullet: Annotated[str, Form()],
    jd_text: Annotated[str, Form()] = "",
    resume_text: Annotated[str, Form()] = "",
):
    result = rewrite_bullet_point(
        bullet=bullet, job_description=jd_text, resume_context=resume_text
    )
    return result
