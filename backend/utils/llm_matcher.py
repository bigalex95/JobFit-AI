# backend/utils/llm_matcher.py

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def run_llm_match(resume_data: dict, jd_data: dict) -> dict:
    """
    Ask Gemini to analyze fit, gaps, and suggestions
    """
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = (
        """
    You are a senior hiring expert. Compare the candidate's resume to the job description.

    Resume:
    """
        + str(resume_data)
        + """

    Job:
    """
        + str(jd_data)
        + """

    Answer:
    1. Does the candidate meet the experience requirement?
    2. Which required skills are missing?
    3. Which skills are present but underemphasized?
    4. What 3 specific, realistic bullet points should they add to their resume?

    Be concise, honest, and helpful.
    """
    )

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
