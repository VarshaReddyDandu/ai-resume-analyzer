import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="Resume Intelligence System", layout="centered")

st.title("AI Resume Analyzer")

resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if resume and job_desc:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    API_URL,
                    files={"resume": resume},
                    data={"job_description": job_desc},
                    timeout=60
                )

                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                    if "raw" in data:
                        st.code(data["raw"])
                else:
                    score = data.get("score", 0)

                    # 🔥 SCORE DISPLAY
                    st.subheader("Match Score")
                    st.progress(score / 100)

                    if score >= 80:
                        st.success(f"{score}% - Strong Match")
                    elif score >= 50:
                        st.warning(f"{score}% - Moderate Match")
                    else:
                        st.error(f"{score}% - Weak Match")

                    # 🔥 MISSING SKILLS
                    st.subheader("Missing Skills")
                    for skill in data.get("missing_skills", []):
                        st.markdown(f"🔻 {skill}")

                    # 🔥 BULLETS
                    st.subheader("Improved Resume Bullets")
                    bullets = data.get("bullets", [])

                    for bullet in bullets:
                        st.markdown(f"✅ {bullet}")

                    st.download_button(
                        label="Download Bullets",
                        data="\n".join(bullets),
                        file_name="resume_bullets.txt"
                    )

            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
    else:
        st.warning("Upload resume and paste job description")