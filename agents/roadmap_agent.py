"""
Roadmap Generator Agent
Generates a month-by-month learning/preparation roadmap.
"""

from utils.gemini_client import generate_json


def generate_roadmap(current_skills: list, target_role: str, months: int = 4) -> dict:
    """
    Returns dict with key:
        roadmap: list of dicts, each with:
            month (int)
            focus_areas (list[str])
            tasks (list[str])
            milestone (str)
    """
    skills_str = ", ".join(current_skills) if current_skills else "None provided"

    prompt = f"""
You are a placement preparation mentor for AIML engineering students in India.

Candidate's current skills: {skills_str}
Target role: {target_role}
Time available: {months} months

Create a month-by-month preparation roadmap covering DSA, core AIML concepts, projects,
resume building, and interview preparation as appropriate.

Return a JSON object with key "roadmap", a list of {months} objects each having:
- "month": integer (1 to {months})
- "focus_areas": list of 2-4 topic areas to focus on this month
- "tasks": list of 3-5 specific actionable tasks for this month
- "milestone": 1 sentence describing what should be achieved by end of this month
"""
    return generate_json(prompt)
