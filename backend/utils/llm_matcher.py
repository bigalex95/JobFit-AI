# backend/utils/llm_matcher.py

import google.generativeai as genai
import json  # ✅ This was missing!
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def run_llm_match(resume_data: dict, jd_data: dict) -> dict:
    """
    Ask Gemini to analyze fit, gaps, and suggestions
    """
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a senior hiring expert. Compare the candidate's resume to the job description.

    Resume:
    {json.dumps(resume_data, indent=2)}

    Job:
    {json.dumps(jd_data, indent=2)}

    Answer:
    1. Does the candidate meet the experience requirement?
    2. List missing required skills (comma-separated)
    3. List underemphasized skills
    4. Suggest 3 realistic, ATS-friendly bullet points to add to their resume.

    RULES:
    - The bullet points MUST include keywords from the MISSING skills.
    - Do NOT suggest generic software engineering experience.
    - Focus on mobile development: Flutter, Dart, Bloc, GraphQL, app store, performance, UI/UX.
    - Use strong action verbs: Developed, Built, Integrated, Optimized, etc.
    - Keep each bullet under 1 line.

    Format:
    • [Action] [specific task] using [missing skill], resulting in [impact].
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        )
        return {"success": True, "feedback": response.text.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}
