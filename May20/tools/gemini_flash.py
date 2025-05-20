import os
import google.generativeai as genai

class GeminiFlashTool:
    name = "llm"

    def __init__(self, api_key=None, model="gemini-1.5-flash"):
        
        self.model = model
        genai.configure(api_key="AIzaSyCi7hA6xxA7lUx-BaUXFpRxipONhGcQfBw")
        self.client = genai.GenerativeModel(model)

    async def complete(self, prompt):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_complete, prompt)

    def _sync_complete(self, prompt):
        response = self.client.generate_content(prompt)
        return response.text.strip()