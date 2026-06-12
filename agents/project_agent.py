"""
Project Recommendation Agent
Suggests projects based on current skills, target role, and domain interest.
"""

from utils.gemini_client import generate_json


def recommend_projects(current_skills: list, target_role: str, domain_interest: str = "") -> dict:
    """
    Returns dict with key:
        projects: list of dicts, each with:
            title (str)
            description (str)
            tech_stack (list[str])
            difficulty (str: Beginner/Intermediate/Advanced)
            resume_value (str)
    """
    skills_str = ", ".join(current_skills) if current_skills else "None provided"
    domain_context = f"Domain interest: {domain_interest}." if domain_interest else ""

    prompt = f"""
You are a project mentor for AIML engineering students preparing for placements in India.

Candidate's current skills: {skills_str}
Target role: {target_role}
{domain_context}

Suggest 5 portfolio projects that would strengthen this candidate's resume for the target role.
Mix difficulty levels (some intermediate, some advanced) and prefer projects involving
Generative AI, LLMs, RAG, Computer Vision, or Agentic AI where relevant since these stand out in 2026.

Return a JSON object with key "projects", a list of 5 objects each having:
- "title": project name
- "description": 2-3 sentence description of what to build
- "tech_stack": list of technologies/tools to use
- "difficulty": one of "Beginner", "Intermediate", "Advanced"
- "resume_value": 1 sentence on why this project stands out to recruiters
"""
    return generate_json(prompt)
