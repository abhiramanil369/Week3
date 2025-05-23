import os
import google.generativeai as genai

def configure_gemini(api_key: str=None):
    if api_key is None:
        api_key="AIzaSyCi7hA6xxA7lUx-BaUXFpRxipONhGcQfBw"
    genai.configure(api_key=api_key)

def summarize_with_gemini(text: str, model_name: str="gemini-1.5-flash-latest")-> str:
    model=genai.GenerativeModel(model_name)
    response=model.generate_content(f"Summarize this:\n{text}")

    return response.text