from fastapi import FastAPI, UploadFile, File, Form
from openai import OpenAI
import os
import json
import PyPDF2

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

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
async def analyze(resume: UploadFile = File(...), job_description: str = Form(...)):
    try:
        resume_text = extract_text_from_pdf(resume)
        job_description = job_description[:1000]

        prompt = f"""
You are a senior resume expert.

Return STRICT JSON:
{{
 "score": number,
 "missing_skills": [],
 "bullets": []
}}

Resume:
{resume_text}

Job:
{job_description}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return only JSON"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )

        text = response.choices[0].message.content

        try:
            return json.loads(text)
        except:
            return {"error": "Invalid JSON", "raw": text}

    except Exception as e:
        return {"error": str(e)}