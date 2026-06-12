"""
Job Matching Agent
Matches candidate profile against a job description and computes a match score.
"""

from utils.gemini_client import generate_json


def match_job(resume_text: str, job_description: str) -> dict:
    """
    Returns dict with keys:
        match_score (int 0-100)
        matching_points (list[str])
        missing_requirements (list[str])
        recommendation (str)
    """
    prompt = f"""
You are a technical recruiter evaluating a candidate against a job description.

Candidate resume text:
\"\"\"
{resume_text}
\"\"\"

Job description:
\"\"\"
{job_description}
\"\"\"

Return a JSON object with these exact keys:
- "match_score": integer 0-100 representing how well the candidate matches this job
- "matching_points": list of 4-6 strings describing how the candidate's profile matches the job requirements
- "missing_requirements": list of 3-6 strings describing requirements from the job description the candidate doesn't clearly meet
- "recommendation": 2-3 sentence overall recommendation for the candidate on whether/how to apply
"""
    return generate_json(prompt)
