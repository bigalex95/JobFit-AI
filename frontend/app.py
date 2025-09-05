import streamlit as st
import requests

# -------------------------------
# Initialize Session State
# -------------------------------
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "resume_file" not in st.session_state:
    st.session_state.resume_file = None
if "result" not in st.session_state:
    st.session_state.result = None
if "show_bullet_rewriter" not in st.session_state:
    st.session_state.show_bullet_rewriter = False

# -------------------------------
# Page Title & Description
# -------------------------------
st.title("🎯 JobFit AI – Optimize Your Resume")

st.write(
    "Upload a job description and your resume to get AI-powered feedback and match analysis."
)

# -------------------------------
# Job Description Input
# -------------------------------
st.subheader("📄 Paste Job Description")
jd_text = st.text_area(
    "Job Description", value=st.session_state.jd_text, height=200, key="jd_input"
)
st.session_state.jd_text = jd_text  # Save to session

# -------------------------------
# Resume Upload
# -------------------------------
st.subheader("📎 Upload Your Resume (PDF)")
resume_file = st.file_uploader("Upload PDF", type=["pdf"], key="resume_uploader")

if resume_file:
    st.session_state.resume_file = resume_file
else:
    st.session_state.resume_file = None

# Display uploaded file
if st.session_state.resume_file:
    st.info(f"✅ {st.session_state.resume_file.name}")

# -------------------------------
# Analyze Fit Button
# -------------------------------
if st.button("🔍 Analyze Fit"):
    if not st.session_state.jd_text.strip() or not st.session_state.resume_file:
        st.error("Please provide both job description and resume.")
    else:
        with st.spinner("🧠 Analyzing with Gemini 2.5 Flash..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/match",
                    data={"jd_text": st.session_state.jd_text},
                    files={
                        "resume_file": (
                            st.session_state.resume_file.name,
                            st.session_state.resume_file.read(),
                            "application/pdf",
                        )
                    },
                )

                if response.status_code == 200:
                    st.session_state.result = response.json()
                    st.success(
                        f"✅ Analysis complete! Match Score: **{st.session_state.result.get('overall_score', 'N/A')}%**"
                    )
                else:
                    st.error(f"❌ Analysis failed: {response.status_code}")
                    st.code(response.text)

            except Exception as e:
                st.error(f"❌ Request failed: {str(e)}")

# -------------------------------
# Show Results (if available)
# -------------------------------
if st.session_state.result:
    result = st.session_state.result

    if "error" in result:
        st.error(f"AI Parsing Failed: {result['error']}")
        st.code(result.get("raw_output", "")[:1000])
    else:
        st.markdown("---")
        st.subheader("📊 Match Summary")

        # Match Score
        st.metric("Match Score", f"{result.get('overall_score', 0)}%")

        # Experience
        parsed_resume = result.get("parsed_resume", {})
        job_summary = result.get("job_summary", {})

        years_exp = parsed_resume.get("years_of_experience", "Unknown")
        req_years = job_summary.get("required_years", "Not specified")

        if isinstance(req_years, (int, float)) and isinstance(years_exp, (int, float)):
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

        # AI Feedback
        st.subheader("🧠 AI-Powered Feedback")
        feedback = result.get("ai_feedback", "")
        for line in feedback.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Fix common OCR/capitalization issues
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

        # Debug: View parsed data
        with st.expander("🔍 View Parsed Resume (Debug)"):
            st.json(parsed_resume)

        with st.expander("📋 View Job Requirements (Debug)"):
            st.json(job_summary)

# -------------------------------
# Optional: Bullet Rewriter (Toggle)
# -------------------------------
st.markdown("---")

# Toggle Button
if st.button("🔤 Toggle Bullet Rewriter"):
    st.session_state.show_bullet_rewriter = not st.session_state.show_bullet_rewriter

# Only show if toggled
if st.session_state.show_bullet_rewriter:
    st.subheader("🔤 AI Bullet Rewriter")
    st.write(
        "Paste a weak bullet point from your resume to make it stronger and ATS-friendly."
    )

    bullet_input = st.text_area("Your Bullet Point", value="", height=100)

    if st.button("Improve This Bullet"):
        if not bullet_input.strip():
            st.warning("Please enter a bullet point.")
        else:
            with st.spinner("🔄 Rewriting with Gemini 2.5 Flash..."):
                try:
                    # Prepare resume context
                    resume_context = ""
                    if st.session_state.result:
                        achievements = st.session_state.result.get(
                            "parsed_resume", {}
                        ).get("key_projects_or_achievements", [])
                        if achievements:
                            resume_context = " ".join(achievements[:2])

                    # Call backend
                    response = requests.post(
                        "http://127.0.0.1:8000/rewrite-bullet",
                        data={
                            "bullet": bullet_input,
                            "jd_text": st.session_state.jd_text,
                            "resume_text": resume_context,
                        },
                    )

                    if response.status_code == 200:
                        rewritten = response.json().get("rewritten", "No suggestion")
                        st.markdown("### ✅ Improved Bullet")
                        st.markdown(f"{rewritten}")
                        st.code(rewritten)  # Easy to copy
                    else:
                        st.error("Failed to rewrite bullet.")
                        st.code(response.text)

                except Exception as e:
                    st.error(f"Error: {str(e)}")
