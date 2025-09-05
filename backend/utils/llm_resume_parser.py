# backend/utils/llm_resume_parser.py

import google.generativeai as genai
import json
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def parse_resume_with_llm(resume_text: str) -> dict:
    """
    Use Gemini to extract structured data from resume
    """
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = (
        """
    You are an expert resume parser. Extract the following fields from the resume text below.
    Return only valid JSON. No markdown, no explanation.

    Fields to extract:
    - name (string)
    - job_title (string, best-fit title)
    - years_of_experience (integer)
    - education (list of strings, e.g., "BSc Computer Engineering")
    - technical_skills (object with keys: languages, ml_frameworks, cloud, mlops, databases, tools)
    - key_projects_or_achievements (list of 3-5 strong bullet points)

    Resume Text:
    """
        + resume_text[:30000]
    )  # Limit length

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        )
        text = response.text.strip()

        # Clean up code block if present
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]

        # Parse JSON
        parsed = json.loads(text)
        return {"success": True, "data": parsed}
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "raw_output": getattr(response, "text", "No response"),
        }
