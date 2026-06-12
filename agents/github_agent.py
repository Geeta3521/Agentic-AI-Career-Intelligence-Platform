"""
GitHub Profile Analysis Agent
Analyzes a GitHub profile's repos (fetched via public GitHub API) for placement readiness.
"""

import requests
from utils.gemini_client import generate_json


def fetch_github_repos(username: str) -> list:
    """Fetch public repo data for a GitHub username."""
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        repos = resp.json()
        if not isinstance(repos, list):
            return []
        return [
            {
                "name": r.get("name"),
                "description": r.get("description"),
                "language": r.get("language"),
                "stars": r.get("stargazers_count", 0),
                "forks": r.get("forks_count", 0),
                "updated_at": r.get("updated_at"),
            }
            for r in repos
        ]
    except requests.exceptions.RequestException:
        return []


def analyze_github_profile(username: str, target_role: str = "") -> dict:
    """
    Returns dict with keys:
        repo_count (int)
        repos_summary (list)
        strengths (list[str])
        improvements (list[str])
        overall_rating (str)
        error (str, optional)
    """
    repos = fetch_github_repos(username)

    if not repos:
        return {
            "error": f"Could not fetch repositories for GitHub user '{username}'. "
                     "Check the username and try again."
        }

    repos_text = "\n".join(
        f"- {r['name']} | Language: {r['language']} | Stars: {r['stars']} | "
        f"Description: {r['description'] or 'No description'}"
        for r in repos[:30]
    )

    role_context = f"The candidate is targeting the role: {target_role}." if target_role else ""

    prompt = f"""
You are a technical recruiter reviewing a candidate's GitHub profile for placement readiness.
{role_context}

Here is a list of the candidate's public repositories:
{repos_text}

Return a JSON object with these exact keys:
- "strengths": list of 3-5 strings describing what looks good on this GitHub profile
- "improvements": list of 4-6 strings with specific, actionable suggestions to improve the profile
  (e.g., add READMEs, pin best repos, add descriptions, remove clutter, add live demo links, etc.)
- "overall_rating": one of "Needs Significant Work", "Average", "Good", "Excellent"
- "standout_repos": list of up to 3 repo names that should be pinned/highlighted
"""
    result = generate_json(prompt)
    result["repo_count"] = len(repos)
    result["repos_summary"] = repos[:30]
    return result
