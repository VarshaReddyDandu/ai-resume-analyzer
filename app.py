from fastapi import FastAPI, UploadFile, File, Form
from openai import OpenAI
import os
import json
import PyPDF2

app = FastAPI()

# ✅ Groq client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# 🔥 Extract text
def extract_text_from_pdf(file):
    try:
        pdf = PyPDF2.PdfReader(file.file)
        text = ""
        for page in pdf.pages[:3]:
            text += page.extract_text() or ""
        return text[:1000]
    except:
        return ""

@app.get("/")
def root():
    return {"message": "API running"}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        resume_text = extract_text_from_pdf(resume)
        jd = job_description.lower()
        res = resume_text.lower()

        # 🔥 Skill-based scoring (REAL LOGIC)
        skills = ["python", "aws", "sql", "machine learning", "pandas"]

        match_count = sum(1 for s in skills if s in res and s in jd)
        score = int((match_count / len(skills)) * 100)
        score = max(score, 60)  # avoid unrealistic low score

        # 🔥 Missing skills
        missing_skills = [s for s in skills if s in jd and s not in res]

        # 🔥 AI bullet improvement
        prompt = f"""
Rewrite resume bullets with STRONG IMPACT.

Rules:
- Add numbers (%, scale, impact)
- Max 20 words each
- Use strong action verbs
- No generic wording

Resume:
{resume_text}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return only bullet points"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=120
        )

        bullets_text = response.choices[0].message.content

        bullets = [b.strip("-• ") for b in bullets_text.split("\n") if b.strip()]

        return {
            "score": score,
            "missing_skills": missing_skills,
            "bullets": bullets[:5]
        }

    except Exception as e:
        return {"error": str(e)}