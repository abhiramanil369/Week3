class BaseAgent:
    def __init__(self, name, tools, role, llm_model=None):
        self.name = name
        self.role = role
        self.tools = {tool.name: tool for tool in tools}
        self.llm = llm_model

    async def act(self, message, context):
        raise NotImplementedError("Each agent must implement act().")