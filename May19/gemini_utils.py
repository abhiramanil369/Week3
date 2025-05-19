import os
import google.generativeai as genai

def configure_gemini(api_key: str=None):
    if api_key is None:
        api_key=os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

def summarize_with_gemini(text: str, model: str="gemini-1.5-flash-latest")-> str:
    response=genai.generate_content(
        model=model,
        contents=[{"role": "user", "parts":[{"text": f"Summarize this:\n{text}"}]}],
    )
    return response.candidates[0]['content']['parts'][0]['text']
