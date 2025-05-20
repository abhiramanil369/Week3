from tools.python_executor import PythonExecutorTool
from tools.linter import PylintLinterTool
from tools.gemini_flash import GeminiFlashTool
from agents.coder import CoderAgent
from agents.debugger import DebuggerAgent
from groupchat import RoundRobinGroupChat

import asyncio

python_executor = PythonExecutorTool()
pylint_linter = PylintLinterTool()
llm_tool = GeminiFlashTool()  # Uses Gemini Flash

coder = CoderAgent(name="Coder", tools=[python_executor, pylint_linter, llm_tool], role="coder")
debugger = DebuggerAgent(name="Debugger", tools=[python_executor, pylint_linter, llm_tool], role="debugger")

group_chat = RoundRobinGroupChat(agents=[coder, debugger])

async def main():
    print("Welcome to Code Debugging Helper!")
    chat_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        response = await group_chat.chat(user_input, chat_history)
        chat_history.append(("user", user_input))
        chat_history.append(("system", response))
        print(f"System: {response}")

if __name__ == "__main__":
    asyncio.run(main())