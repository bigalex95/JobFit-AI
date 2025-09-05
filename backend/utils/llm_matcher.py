# backend/utils/llm_matcher.py

import google.generativeai as genai
import json
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def run_llm_match(resume_data: dict, jd_data: dict) -> dict:
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a senior hiring expert. Compare the candidate's resume to the job description.

    Resume:
    {json.dumps(resume_data, indent=2)}

    Job:
    {json.dumps(jd_data, indent=2)}

    Answer in valid JSON format:
    {{
      "experience_met": true/false,
      "missing_required_skills": "Skill1, Skill2",
      "underemphasized_skills": "Skill3, Skill4",
      "suggested_bullet_points": [
        "• Developed mobile apps using Flutter and Dart..."
      ]
    }}
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        )

        # Try to parse as JSON
        try:
            parsed = json.loads(response.text.strip())
            return {"success": True, "feedback": parsed}  # Return as dict
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return raw text as fallback
            return {
                "success": False,
                "error": f"LLM returned invalid JSON: {str(e)}",
                "feedback": response.text.strip(),  # Raw string fallback
            }

    except Exception as e:
        return {"success": False, "error": str(e)}
