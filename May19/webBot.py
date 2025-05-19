import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from gemini_utils import configure_gemini, summarize_with_gemini

async def fetch_web_content(url: str) -> str:
    options=Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    try:
        driver= webdriver.Chrome(options=options)
        driver.get(url)
        await asyncio.sleep(2)
        content= driver.page_source
        driver.quit()
        return content
    except WebDriverException as e:
        return f"Error fetching content from {url}: {e}"

async def summarize_content(content:str) -> str:
    return await asyncio.to_thread(summarize_with_gemini,content)
    