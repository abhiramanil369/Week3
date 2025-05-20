from base_agent import BaseAgent

class CoderAgent(BaseAgent):
    async def act(self, message, context):
        # Use LLM for code generation
        prompt = f"""You are a helpful coding assistant. Write or improve Python code as requested by the user.
Request: {message}
Context: {context}
Output ONLY the code (no explanations, no comments unless asked).
"""
        llm = self.tools.get("llm")
        if llm:
            return await llm.complete(prompt)
        return "# LLM is not available."