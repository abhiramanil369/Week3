from base_agent import BaseAgent

class DebuggerAgent(BaseAgent):
    
    def __init__(self,name,tools):
        super().__init__(name,tools,role="debugger")
    
    async def act(self,message,context):

        code=context.get("latest_code",message)
        lint_report=await self.tools["linter"].lint(code)
        exec_report=await self.tools["executor"].execute(code)
        feedback=f"Linter Report: \n{lint_report}\n\nExecution Report: \n{exec_report}"

        return feedback
    

    