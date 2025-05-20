import asyncio
from agents.coder import CoderAgent
from agents.debugger import DebuggerAgent
from tools.python_executor import PythonExecutorTool
from tools.linter import PylintLinterTool
from groupchat import RoundRobinGroupChat

python_executor= PythonExecutorTool()
pylint_linter=PylintLinterTool()

coder=CoderAgent(name="Coder",tools=[python_executor,pylint_linter])
debugger=DebuggerAgent(name="Debugger",tools=[python_executor,pylint_linter])

group_chat=RoundRobinGroupChat(
    agents=[coder,debugger],
    llm="gemini-flash-1.5"
)

async def main():
    print("Welcome to Code Debugging Helper!")
    chat_history=[]
    while True:
        user_input=input("You: ")
        if user_input.lower() in ['exit','quit']:
            break
        response=await group_chat.chat(user_input,chat_history)
        chat_history.append(("user",user_input))
        chat_history.append(("system",response))
        print(f"System: {response}")


if __name__=="__main__":
    asyncio.run(main())