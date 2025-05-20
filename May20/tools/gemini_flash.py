import os
import google.generativeai as genai

class GeminiFlashTool:
    name = "llm"

    def __init__(self, api_key=None, model="gemini-1.5-flash"):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.model = model
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(model)

    async def complete(self, prompt):
        # The Google SDK is synchronous, so run in thread for async
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_complete, prompt)

    def _sync_complete(self, prompt):
        response = self.client.generate_content(prompt)
        return response.text.strip()