# frontend/app.py

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
        with st.spinner("🔍 Analyzing with AI..."):

            # Call FastAPI
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

            # Show error if LLM parsing failed
            if "error" in result:
                st.error(f"AI Parsing Failed: {result['error']}")
                st.code(result.get("raw_output", "")[:1000])
                st.stop()

            # ✅ Match Score
            score = result.get("overall_score", 0)
            st.success(f"✅ Match Score: **{score}%**")

            # 📊 Parsed Experience Check
            parsed_resume = result.get("parsed_resume", {})
            job_summary = result.get("job_summary", {})

            years_exp = parsed_resume.get("years_of_experience", "Unknown")
            req_years = job_summary.get("required_years", "Not specified")

            if isinstance(req_years, (int, float)) and isinstance(
                years_exp, (int, float)
            ):
                if years_exp >= req_years:
                    st.success(
                        f"✅ Experience: You have **{years_exp}+ years**, meets requirement of {req_years}+ years"
                    )
                else:
                    st.warning(
                        f"⚠️ Experience: You have **{years_exp} years**, but job requires **{req_years}+ years**"
                    )
            else:
                st.info("📊 Experience: Could not determine exact years.")

            # 💬 AI Feedback (Gaps & Suggestions)
            feedback = result.get("ai_feedback", "")
            st.subheader("🧠 AI-Powered Feedback")

            for line in feedback.split("\n"):
                line = line.strip()
                if not line:
                    continue
                # Fix common rendering issues
                line = (
                    line.replace("Doveloped", "Developed")
                    .replace("DeveLoped", "Developed")
                    .replace("Leaming", "Learning")
                    .replace("Ml", "ML")
                    .replace("Nlp", "NLP")
                    .replace("Mlops", "MLOps")
                )

                if (
                    line.startswith("1.")
                    or line.startswith("2.")
                    or line.startswith("3.")
                    or line.startswith("4.")
                ):
                    st.markdown(f"**{line}**")
                elif line.startswith("•") or line[0].isdigit():
                    st.markdown(f"- {line}")

            # 📥 Optional: Show raw parsed data (for debugging)
            with st.expander("📄 View Parsed Resume (Debug)"):
                st.json(parsed_resume)

            with st.expander("📋 View Job Requirements (Debug)"):
                st.json(job_summary)

        else:
            st.error("❌ Analysis failed.")
            st.code(response.text)
