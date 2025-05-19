import asyncio
from webBot import fetch_web_content, summarize_content

async def round_robin_groupchat(url: str):
    print(f"Researcher: Fetching content from {url}")
    content=await fetch_web_content(url)
    print(f"Researcher: Contents fetched. Passing to Summarizer......")

    print("Summarizer: Generating summary...")
    summary=await summarize_content(content)
    print("Summarizer: Summary completed.\n")
    return summary
