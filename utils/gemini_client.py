"""
Gemini LLM client wrapper used by all agents.
"""

import json
import re
import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME


def _configure():
    if not GEMINI_API_KEY or GEMINI_API_KEY == "PASTE_YOUR_GEMINI_API_KEY_HERE":
        raise ValueError(
            "Gemini API key not set. Open config.py and paste your API key, "
            "or set the GEMINI_API_KEY environment variable."
        )
    genai.configure(api_key=GEMINI_API_KEY)


def get_model():
    _configure()
    return genai.GenerativeModel(MODEL_NAME)


def generate_text(prompt: str, temperature: float = 0.7) -> str:
    """Generate plain text response from Gemini."""
    model = get_model()
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=temperature),
    )
    return response.text.strip()


def generate_json(prompt: str, temperature: float = 0.4) -> dict:
    """
    Generate a response and parse it as JSON.
    Handles cases where Gemini wraps JSON in markdown code fences.
    """
    full_prompt = (
        prompt
        + "\n\nIMPORTANT: Respond ONLY with valid JSON. "
        "Do not include any explanation, preamble, or markdown formatting."
    )
    raw = generate_text(full_prompt, temperature=temperature)

    # Strip markdown code fences if present
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to extract the first {...} or [...] block
        match = re.search(r"(\{.*\}|\[.*\])", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        # Fall back: return raw text wrapped in dict
        return {"raw_response": raw, "parse_error": True}
