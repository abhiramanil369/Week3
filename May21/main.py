import asyncio
from crewai import Agent
from crewai_tools import GeminiTool, CodeInterpreterTool, FileReadTool, FileWriteTool
from google.cloud import storage
import os

# -- Configure Google Cloud credentials before running this script --
# export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"

# Define tools
gemini = GeminiTool()
code_interpreter = CodeInterpreterTool()
file_reader = FileReadTool()
file_writer = FileWriteTool()

# Data Fetcher agent: fetches CSV data from Google Cloud Storage
class DataFetcherAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Data Fetcher",
            description="Fetches CSV data from Google Cloud Storage.",
            llm=gemini,
            tools=[file_reader, file_writer],
            async_mode=True
        )

    async def fetch_data(self, bucket_name: str, blob_name: str, local_path: str = "temp.csv") -> str:
        # Download CSV file from GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(local_path)
        # Read the file contents
        return await self.tools[0].read(local_path)

# Analyst agent: analyzes CSV data using pandas & matplotlib
class AnalystAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Analyst",
            description="Analyzes data using pandas and matplotlib.",
            llm=gemini,
            tools=[code_interpreter, file_writer],
            async_mode=True
        )

    async def analyze_data(self, csv_content: str, output_dir: str = "outputs") -> list:
        code = f'''
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

os.makedirs("{output_dir}", exist_ok=True)
df = pd.read_csv(io.StringIO("""{csv_content}"""))

summary = df.describe().to_string()
plots = []
for col in df.select_dtypes(include='number').columns:
    plt.figure()
    df[col].hist(bins=20)
    plt.title(f"Histogram of {{col}}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    filepath = f"{output_dir}/hist_{{col}}.png"
    plt.savefig(filepath)
    plt.close()
    plots.append(filepath)

with open(f"{output_dir}/summary.txt", "w") as f:
    f.write(summary)

plots.append(f"{output_dir}/summary.txt")
plots
'''
        return await self.tools[0].interpret(code)

# Group chat for agent orchestration
from crewai.process import RoundRobinGroupChat

class DataAnalysisGroupChat(RoundRobinGroupChat):
    def __init__(self, agents):
        super().__init__(agents=agents, async_mode=True)

# Async pipeline entrypoint
async def main(bucket_name: str, blob_name: str):
    data_fetcher = DataFetcherAgent()
    analyst = AnalystAgent()
    group = DataAnalysisGroupChat([data_fetcher, analyst])

    csv_content = await data_fetcher.fetch_data(bucket_name, blob_name)
    output_files = await analyst.analyze_data(csv_content)
    print("Analysis complete. Generated files:")
    for file in output_files:
        print(f"- {file}")

if __name__ == "__main__":
    # Usage: python data_analysis_pipeline_gcloud.py <bucket_name> <blob_name>
    import sys
    if len(sys.argv) < 3:
        print("Usage: python data_analysis_pipeline_gcloud.py <bucket_name> <blob_name>")
    else:
        asyncio.run(main(sys.argv[1], sys.argv[2]))