class BaseAgent:
    def __init__(self,name,tools,role):
        self.name=name
        self.role=role
        self.tools={tool.name: tool for tool in tools}
        self.llm=self.init_llm()

    def init_llm(self):
        class GeminiLLM:
            async def generate_code(self,prompt):
                return "#Gemini-generated code for: "+prompt
        return GeminiLLM()
        
    async def act(self,message,context):
        raise NotImplementedError("Each agent must implement asct()")
    