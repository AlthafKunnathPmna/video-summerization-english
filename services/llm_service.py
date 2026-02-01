import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

# model = genai.GenerativeModel("gemini-1.5-flash")
model = genai.GenerativeModel("models/gemini-2.5-flash")

def gemini_reason(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()
