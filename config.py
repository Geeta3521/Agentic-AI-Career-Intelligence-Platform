"""
Central configuration for AI Career Copilot.
Put your Gemini API key here OR set it as an environment variable GEMINI_API_KEY.
Get a free key from: https://aistudio.google.com/app/apikey
"""
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

APP_TITLE = "AI Career Copilot"
APP_ICON = "🚀"
