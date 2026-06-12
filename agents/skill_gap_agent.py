"""
Skill Gap Agent
Compares user's current skills against a target role and identifies gaps.
"""

from utils.gemini_client import generate_json


def analyze_skill_gap(current_skills: list, target_role: str) -> dict:
    """
    Returns dict with keys:
        required_skills (list[str])
        matched_skills (list[str])
        missing_skills (list[str])
        priority_skills (list[str])  - top 3 to learn first
        match_percentage (int 0-100)
    """
    skills_str = ", ".join(current_skills) if current_skills else "None provided"

    prompt = f"""
You are a career advisor specializing in AIML and software engineering placements in India.

Candidate's current skills: {skills_str}
Target role: {target_role}

Return a JSON object with these exact keys:
- "required_skills": list of 10-15 key skills typically required for this role
- "matched_skills": list of skills from the candidate's current skills that match required skills
- "missing_skills": list of important skills the candidate is missing for this role
- "priority_skills": list of the top 3 missing skills the candidate should learn first, in order of priority
- "match_percentage": integer 0-100 representing overall skill match for this role
"""
    return generate_json(prompt)
