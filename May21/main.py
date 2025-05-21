import asyncio
import pandas as pd
import matplotlib.pyplot as plt

from autogen import tool, UserProxyAgent, GroupChatManager
from autogen.agentchat.contrib.gemini import GeminiAgent

# ----------- Tools -----------

@tool
def load_csv(filepath: str):
    """Load CSV and return summary statistics."""
    df = pd.read_csv(filepath)
    return {
        "summary": df.describe().to_string(),
        "columns": df.columns.tolist(),
        "shape": df.shape
    }

@tool
def generate_plot(filepath: str, x_col: str, y_col: str, output_path: str = "plot.png"):
    """Generate a plot for given columns and save it."""
    df = pd.read_csv(filepath)
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_col], df[y_col], marker='o')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{y_col} vs {x_col}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    return f"Plot saved at {output_path}"

# ----------- Gemini LLM Config -----------

gemini_config = {
    "model": "gemini/gemini-flash",
    "api_key": "your-gemini-api-key-here"  # <-- Replace with your Gemini Flash API key
}

# ----------- Agents -----------

data_fetcher = GeminiAgent(
    name="DataFetcher",
    llm_config={"config_list": [gemini_config]},
    system_message="You load CSV files and return summaries.",
    tools=[load_csv]
)

analyst = GeminiAgent(
    name="Analyst",
    llm_config={"config_list": [gemini_config]},
    system_message="You generate visualizations from CSV data.",
    tools=[generate_plot]
)

user_agent = UserProxyAgent(name="User", human_input_mode="ALWAYS")

# ----------- Group Chat Manager -----------

from autogen.agentchat.contrib.multimodal import RoundRobinGroupChat

group_chat = RoundRobinGroupChat(
    agents=[user_agent, data_fetcher, analyst],
    max_round=5
)

manager = GroupChatManager(groupchat=group_chat)

# ----------- Async Runner -----------

async def run_pipeline():
    await user_agent.a_initiate_chat(
        manager=manager,
        message="Please load the CSV file 'sales_data.csv' and then generate a plot of 'Date' vs 'Sales'."
    )

if __name__ == "__main__":
    asyncio.run(run_pipeline())
