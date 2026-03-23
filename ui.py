import streamlit as st
import requests

# 🔥 USE YOUR LIVE BACKEND
API_URL = "https://ai-resume-analyzer-verm.onrender.com/analyze"

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.markdown("# 🚀 AI Resume Analyzer")

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
                else:
                    score = data.get("score", 0)

                    st.subheader("📊 Match Score")
                    st.progress(score / 100)
                    st.write(f"{score}%")

                    st.subheader("⚠️ Missing Skills")
                    for skill in data.get("missing_skills", []):
                        st.markdown(f"- {skill}")

                    st.subheader("✨ Improved Bullets")
                    bullets = data.get("bullets", [])
                    for b in bullets:
                        st.markdown(f"✅ {b}")

                    st.download_button(
                        "Download Bullets",
                        "\n".join(bullets),
                        file_name="resume.txt"
                    )

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Upload resume + paste job description")