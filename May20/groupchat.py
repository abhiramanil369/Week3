class RoundRobinGroupChat:
    def __init__(self,agents,llm):
        self.agents=agents
        self.llm=llm
        self.next_index=0
    
    async def chat(self,user_input,chat_history):
        context=self._build_context(chat_history)
        agent=self.agents[self.next_index]
        self.next_index=(self.next_index+1)% len(self.agents)
        response =await agent.act(user_input,context)
        return response
    def _build_context(self,chat_history):
        context={}
        
        for role, msg in reversed(chat_history):
            if role == "system" and "```python" in msg:
                context["latest_code"]=msg
                break
        
        return context
    