import os
from dotenv import load_dotenv
from gemini_utils import configure_gemini
from group_chat import round_robin_groupchat

def main():

    load_dotenv()
    configure_gemini()

    url=input("Enter the URL to research and summarize: ").strip()

    import asyncio
    summary=asyncio.run(round_robin_groupchat(url))
    print("\n=====SUMMARY=====\n")
    print(summary)

if __name__=="__main__":
    main()