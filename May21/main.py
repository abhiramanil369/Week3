import asyncio
import pandas as pd
import matplotlib.pyplot as plt
import json
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession


PROJECT_ID = "data-pipeline-460515"
REGION = "us-central1"  
MODEL = "gemini-1.5-flash"
SERVICE_ACCOUNT_FILE = "key.json" 

# === AUTHENTICATION ===
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
authed_session = AuthorizedSession(credentials)

async def call_gemini_flash(prompt: str):
    endpoint = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/publishers/google/models/{MODEL}:predict"
    payload = {
        "instances": [
            {
                "prompt": prompt,
            }
        ],
        "parameters": {
            "temperature": 0.7,
            "maxOutputTokens": 500,
            "topP": 0.8,
            "topK": 40
        }
    }
    response = authed_session.post(endpoint, json=payload)
    response.raise_for_status()
    return response.json()

async def data_fetcher(csv_file):
    df = pd.read_csv(csv_file, parse_dates=["Date"])
    df.set_index("Date", inplace=True)
    print("Data sample:\n", df.head())
    return df

async def analyst(df):
    summary = df.describe()
    df["Sales"].plot(kind='line', title="Sales Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.savefig("output_plot.png")
    plt.close()
    return summary

async def main(csv_file):
    print(f"Loading data from {csv_file}...")
    df = await data_fetcher(csv_file)
    
    print("Analyzing data and creating plot...")
    analysis = await analyst(df)

    prompt = f"Here is a dataset summary:\n{analysis.to_string()}\nPlease provide insights or observations."
    
    print("Sending analysis prompt to Gemini Flash...")
    result = await call_gemini_flash(prompt)
    
    print("Gemini Flash response:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    import sys
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "sales_data.csv"
    asyncio.run(main(csv_file))
