import streamlit as st
import requests

st.title("🎯 JobFit AI – Optimize Your Resume")

st.write("Upload a job description and your resume to see how well you match!")

# Input: Job Description
jd_text = st.text_area("Paste Job Description", height=200)

# Input: Resume PDF
resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if st.button("Analyze Fit"):
    if not jd_text or not resume_file:
        st.error("Please provide both job description and resume.")
    else:
        with st.spinner("Analyzing..."):
            response = requests.post(
                "http://127.0.0.1:8000/match",
                data={"jd_text": jd_text},
                files={
                    "resume_file": (
                        resume_file.name,
                        resume_file.read(),
                        "application/pdf",
                    )
                },
            )

        if response.status_code == 200:
            result = response.json()

            st.success(f"Match Score: {result['overall_score']}%")

            # Missing Skills
            missing = result["skill_match"]["missing_skills"]
            if missing:
                st.warning("⚠️ Missing Skills:")
                for s in missing:
                    st.markdown(f"- **{s['skill']}** (relevance: {s['match_score']})")
            else:
                st.success("✅ All required skills are covered!")

            # Experience Match
            exp = result["experience_match"]
            required_years = exp.get("required_years", 0)

            if exp["meets_requirement"] and required_years > 0:
                st.success(
                    f"✅ Experience: You have {exp['resume_years']}, required {required_years}+ years"
                )
            elif required_years > 0:
                st.error(
                    f"❌ You have {exp['resume_years']}, but job requires {required_years}+ years"
                )
            else:
                st.warning(
                    "⚠️ Could not detect required experience from job description."
                )

            # AI Suggestions
            if "ai_suggestions" in result:
                st.subheader("🧠 AI-Powered Suggestions")

                # Clean up bullet points
                suggestions = result["ai_suggestions"]
                for line in suggestions.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    # Fix common OCR/case issues
                    line = line.replace("DeveLoped", "Developed").replace(
                        "Doveloped", "Developed"
                    )
                    line = line.replace("Leaming", "Learning").replace("Ml", "ML")
                    if line.startswith("•") or line[0].isdigit():
                        st.markdown(f"- {line}")

            # Suggestions
            st.subheader("📌 Suggestions")
            if missing:
                st.markdown("Add these skills to your resume:")
                for m in missing:
                    st.code(f"• Developed ML solutions using {m['skill']}.")
        else:
            st.error("Analysis failed.")
