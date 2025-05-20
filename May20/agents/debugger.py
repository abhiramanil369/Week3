from base_agent import BaseAgent

class DebuggerAgent(BaseAgent):
    async def act(self, message, context):
        # Use LLM for debugging help
        prompt = f"""You are an expert Python debugger. Analyze the following user input, point out bugs or improvements, and suggest fixes.
User input: {message}
Context: {context}
Give a short explanation and corrected code if needed.
"""
        llm = self.tools.get("llm")
        if llm:
            return await llm.complete(prompt)
        return "# LLM is not available."