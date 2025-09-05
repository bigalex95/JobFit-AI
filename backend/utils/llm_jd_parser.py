# backend/utils/llm_jd_parser.py

import google.generativeai as genai
import json
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def parse_jd_with_llm(jd_text: str) -> dict:
    """
    Use Gemini to extract structured requirements from job description
    """
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = (
        """
    You are an expert job analyst. Extract the following from the job description.
    Return only valid JSON. No markdown, no explanation.

    Fields:
    - job_title (string)
    - required_years (integer)
    - required_education (list of strings)
    - required_skills (object with: languages, ml_frameworks, cloud, mlops, nlp, cv, etc.)
    - nice_to_have_skills (list)
    - key_responsibilities (list of 3-5 bullets)

    Job Description:
    """
        + jd_text[:10000]
    )

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        )
        text = response.text.strip()

        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]

        parsed = json.loads(text)
        return {"success": True, "data": parsed}
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "raw_output": getattr(response, "text", "No response"),
        }
