import streamlit as st
import requests

API_URL = "https://ai-resume-analyzer-verm.onrender.com/analyze"

st.set_page_config(page_title="AI Resume Intelligence", layout="centered")

st.title("🚀 AI Resume Intelligence Platform")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if not uploaded_file or not job_description:
        st.warning("Please upload resume and enter job description")
    else:
        with st.spinner("Analyzing..."):
            try:
                # 🔥 Proper file format
                files = {
                    "resume": (uploaded_file.name, uploaded_file, "application/pdf")
                }

                response = requests.post(
                    API_URL,
                    files=files,
                    data={"job_description": job_description},
                    timeout=60
                )

                # 🔥 Check backend health
                if response.status_code != 200:
                    st.error(f"Backend error: {response.status_code}")
                    st.stop()

                try:
                    data = response.json()
                except:
                    st.error("Invalid response from server")
                    st.stop()

                if "error" in data:
                    st.error(data["error"])
                    st.stop()

                # 🔥 Safe extraction
                score = data.get("score", 0)
                missing_skills = data.get("missing_skills", [])
                bullets = data.get("bullets", [])

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
                if bullets:
                    for b in bullets:
                        st.markdown(f"✅ {b}")
                else:
                    st.info("No suggestions generated")

                # 🔥 Insight
                st.markdown("## 🧠 AI Insight")
                if missing_skills:
                    st.info(f"Improve your resume by adding: {', '.join(missing_skills)}")
                else:
                    st.success("Your resume aligns well with this role")

            except requests.exceptions.Timeout:
                st.error("Server is slow. Try again.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Check deployment.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")