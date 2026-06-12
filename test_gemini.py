import google.generativeai as genai

import os

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Hello")
    print("SUCCESS:")
    print(response.text)
except Exception as e:
    print("ERROR:")
    print(e)