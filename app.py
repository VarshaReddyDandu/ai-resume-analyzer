@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        resume_text = extract_text_from_pdf(resume)
        
        if not resume_text:
            return {"error": "Could not extract text from resume"}

        res = resume_text.lower()
        jd = job_description.lower()

        # 🔥 Better skill pool (expanded)
        common_skills = [
            "python", "sql", "aws", "machine learning", "ml",
            "pandas", "docker", "kubernetes", "spark", "kafka",
            "data pipelines", "deep learning", "nlp", "api",
            "fastapi", "flask", "tensorflow", "pytorch"
        ]

        # 🔥 Smarter matching (partial match support)
        jd_skills = [s for s in common_skills if any(word in jd for word in s.split())]

        # 🔥 Missing skills
        missing_skills = [s for s in jd_skills if s not in res]

        # 🔥 Score calculation
        match_count = sum(1 for s in jd_skills if s in res)

        score = int((match_count / len(jd_skills)) * 100) if jd_skills else 70
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
                {"role": "system", "content": "Return ONLY 5 bullet points"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )

        # 🔥 Safe extraction
        bullets_text = ""
        if response and response.choices:
            bullets_text = response.choices[0].message.content or ""

        # 🔥 Strong parsing
        bullets = [
            b.strip("-•1234567890. ").strip()
            for b in bullets_text.split("\n")
            if len(b.strip()) > 5
        ]

        return {
            "score": score,
            "missing_skills": missing_skills,
            "bullets": bullets[:5]
        }

    except Exception as e:
        return {"error": str(e)}