from fastapi import FastAPI, UploadFile, File, Form
from openai import OpenAI
import os
import PyPDF2

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# 🔥 Extract text from PDF
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
        res = resume_text.lower()
        jd = job_description.lower()

        # 🔥 Smart skill pool
        common_skills = [
            "python", "sql", "aws", "machine learning", "pandas",
            "docker", "kubernetes", "spark", "kafka",
            "real-time", "data pipelines", "deep learning"
        ]

        # 🔥 Extract JD skills dynamically
        jd_skills = [s for s in common_skills if s in jd]

        # 🔥 Missing skills
        missing_skills = [s for s in jd_skills if s not in res]

        # 🔥 Score
        match_count = sum(1 for s in jd_skills if s in res)

        if jd_skills:
            score = int((match_count / len(jd_skills)) * 100)
        else:
            score = 70

        score = max(score, 40)

        # 🔥 AI bullet improvement
        prompt = f"""
Rewrite resume bullets with strong impact.

Rules:
- Add numbers (% or scale)
- Max 20 words
- Use strong verbs (Built, Improved, Reduced)
- No generic text

Resume:
{resume_text}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return bullet points only"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=120
        )

        bullets_text = response.choices[0].message.content
        bullets = [b.strip("-• ") for b in bullets_text.split("\n") if b.strip()]

        return {
            "sc9ore": score,
            "missing_skills": missing_skills,
            "bullets": bullets[:5]
        }

    except Exception as e:
        return {"error": str(e)}