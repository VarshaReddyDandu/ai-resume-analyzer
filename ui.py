import streamlit as st
import requests

API_URL = "https://ai-resume-analyzer-verm.onrender.com/analyze"

st.set_page_config(page_title="AI Resume Intelligence", layout="centered")

st.title("🚀 AI Resume Intelligence Platform")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if uploaded_file and job_description:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    API_URL,
                    files={"resume": uploaded_file},
                    data={"job_description": job_description},
                    timeout=60
                )

                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    score = data["score"]
                    missing_skills = data["missing_skills"]
                    bullets = data["bullets"]

                    # 🔥 Score UI
                    st.markdown("## 📊 Match Score")
                    st.progress(score / 100)

                    if score > 80:
                        st.success(f"{score}% - Strong Match")
                    elif score > 60:
                        st.warning(f"{score}% - Moderate Match")
                    else:
                        st.error(f"{score}% - Weak Match")

                    # 🔥 Missing skills
                    st.markdown("## ⚠️ Missing Skills")
                    if missing_skills:
                        for skill in missing_skills:
                            st.markdown(f"🔴 {skill}")
                    else:
                        st.success("No major missing skills")

                    # 🔥 Improved bullets
                    st.markdown("## ✨ Improved Resume Bullets")
                    for b in bullets:
                        st.markdown(f"✅ {b}")

                    # 🔥 Insight
                    st.markdown("## 🧠 AI Insight")
                    if missing_skills:
                        st.info(f"Improve your resume by adding: {', '.join(missing_skills)}")
                    else:
                        st.success("Your resume aligns well with this role")

            except Exception as e:
                st.error(f"Connection failed: {e}")