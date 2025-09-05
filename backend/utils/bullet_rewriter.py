# backend/utils/bullet_rewriter.py

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def rewrite_bullet_point(
    bullet: str, job_description: str = "", resume_context: str = ""
) -> dict:
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a resume optimization expert. Rewrite the following bullet point to be:
    - Stronger, more specific, and achievement-oriented
    - Include relevant keywords from the job description
    - Use strong action verbs: Developed, Led, Built, Optimized, etc.
    - Add metrics if possible (even estimated)
    - Keep under 1 line

    Original Bullet:
    {bullet}

    Job Description (for keywords):
    {job_description[:500]}

    Resume Context (for realism):
    {resume_context[:500]}

    Return only the improved bullet point. No explanation.
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        )
        rewritten = response.text.strip()

        # Clean output
        if rewritten.startswith("•"):
            rewritten = rewritten[1:].strip()

        return {"success": True, "rewritten": f"• {rewritten}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
