"""
Resume Analyzer Agent
Analyzes resume text and returns ATS score, weak areas, missing keywords, suggestions.
"""

from utils.gemini_client import generate_json


def analyze_resume(resume_text: str, target_role: str = "") -> dict:
    """
    Analyze a resume and return structured feedback.

    Returns dict with keys:
        ats_score (int 0-100)
        strengths (list[str])
        weak_areas (list[str])
        missing_keywords (list[str])
        suggestions (list[str])
        extracted_skills (list[str])
    """
    role_context = f"The candidate is targeting the role: {target_role}." if target_role else ""

    prompt = f"""
You are an expert ATS (Applicant Tracking System) resume reviewer and technical recruiter
for AIML / Software Engineering roles in India.

{role_context}

Analyze the following resume text and return a JSON object with these exact keys:
- "ats_score": integer between 0 and 100 representing how well this resume would pass ATS screening
- "strengths": list of 3-5 strings describing what is good about the resume
- "weak_areas": list of 3-5 strings describing weaknesses (formatting, content, clarity, impact, etc.)
- "missing_keywords": list of 5-10 important keywords/skills missing for AIML/SDE roles that should be added if relevant
- "suggestions": list of 5-7 specific, actionable improvement suggestions
- "extracted_skills": list of all technical skills, tools, and frameworks found in the resume

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""
    return generate_json(prompt)
