"""
AI Interview Agent
Conducts a text-based mock interview: generates questions and evaluates answers.
"""

from utils.gemini_client import generate_json


def generate_interview_questions(target_role: str, skills: list, num_questions: int = 5) -> dict:
    """
    Returns dict with key:
        questions: list of dicts with:
            question (str)
            type (str: Technical/Behavioral/HR)
    """
    skills_str = ", ".join(skills) if skills else "general AIML/CS fundamentals"

    prompt = f"""
You are an interviewer for a {target_role} position at a tech company in India.
The candidate's skills include: {skills_str}.

Generate {num_questions} mock interview questions, mixing technical, behavioral, and HR questions
(majority technical, relevant to {target_role} and the candidate's skills).

Return a JSON object with key "questions", a list of {num_questions} objects each having:
- "question": the interview question text
- "type": one of "Technical", "Behavioral", "HR"
"""
    return generate_json(prompt)


def evaluate_answer(question: str, answer: str, target_role: str) -> dict:
    """
    Returns dict with keys:
        technical_score (int 0-10)
        communication_score (int 0-10)
        confidence_score (int 0-10)
        feedback (str)
        ideal_answer_points (list[str])
    """
    prompt = f"""
You are an expert interviewer evaluating a candidate's answer for a {target_role} interview.

Question: {question}
Candidate's Answer: {answer}

Evaluate the answer and return a JSON object with these exact keys:
- "technical_score": integer 0-10 (technical correctness/depth; for behavioral/HR questions, score relevance and structure)
- "communication_score": integer 0-10 (clarity, structure, articulation)
- "confidence_score": integer 0-10 (how confident and assertive the answer sounds)
- "feedback": 2-3 sentences of constructive feedback
- "ideal_answer_points": list of 3-4 key points an ideal answer would cover
"""
    return generate_json(prompt)
