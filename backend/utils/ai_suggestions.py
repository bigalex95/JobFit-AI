# backend/utils/ai_suggestions.py

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_resume_suggestions(
    jd_text: str, resume_text: str, missing_skills: list, experience_gap: dict
) -> str:
    """
    Ask Gemini to suggest how to improve the resume
    """
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a senior career coach helping a Machine Learning Scientist optimize their resume for a competitive role.
    The candidate has strong experience but may not be highlighting key terms from the job description.

    Below is the job description, a snippet of their resume, the missing skills, and experience gap.

    Your task:
    - Suggest 3-5 **specific, realistic, and ATS-friendly** bullet points to add.
    - Use **strong action verbs**: Developed, Led, Built, Deployed, Optimized, etc.
    - Include **keywords** from missing skills.
    - Base suggestions on their actual experience (e.g., if they used LangChain, suggest LLM fine-tuning).
    - Do NOT lie, but help them **rephrase or highlight hidden experience**.

    Job Description:
    {jd_text}

    Resume Snippet:
    {resume_text[:1500]}

    Missing Skills: {', '.join([s['skill'] for s in missing_skills]) if missing_skills else 'None'}

    Experience Required: {experience_gap.get('required_years', 'Unknown')}+ years
    Candidate Experience: {experience_gap.get('resume_years', 'Unknown')}

    Format:
    • [Action verb] [specific task] using [keyword], resulting in [impact].
    • ...
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        )
        return response.text.strip()
    except Exception as e:
        return f"AI suggestion failed: {str(e)}"
