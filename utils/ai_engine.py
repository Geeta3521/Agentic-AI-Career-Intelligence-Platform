"""utils/ai_engine.py — All Gemini API calls"""
import re
import json
import streamlit as st
import google.generativeai as genai


def _model():
    import os
    key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    if not key or key == "your-gemini-api-key-here":
        st.error("⚠️ Add your GEMINI_API_KEY to `.streamlit/secrets.toml`  |  Get free key → https://aistudio.google.com/app/apikey")
        st.stop()
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-1.5-flash")


def ai_text(prompt: str) -> str:
    return _model().generate_content(prompt).text


def ai_json(prompt: str) -> dict:
    raw = ai_text(prompt)
    clean = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()
    try:
        return json.loads(clean)
    except Exception:
        m = re.search(r'\{.*\}', clean, re.DOTALL)
        if m:
            return json.loads(m.group())
        raise ValueError(f"Could not parse AI JSON. Raw:\n{raw[:400]}")
