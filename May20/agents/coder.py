from base_agent import BaseAgent

class CoderAgent(BaseAgent):
    def __init__(self,name,tools):
        super().__init__(name,tools,role="coder")

    async def act(self,message,context):
        prompt=(
            f"You are the Coder. Write or improve the following Python code:\n"
            f"{message}\n"
            f"Consider feedback and debugging info from the context.\n"
        )
        code=await self.llm.generate_code(prompt)
        return code