from fastapi import FastAPI
import pandas as pd
import yaml

CONFIG_PATH = "/Users/pnupadya/Documents/learn/git_repos/data_analysis_agent/config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

app = FastAPI()

@app.get("/weather")
def get_weather():
    df = pd.read_csv(config["files"]["weather_csv"])
    return df.to_dict(orient="records")

# Run with: uvicorn src.weather_api:app --host 0.0.0.0 --port 9000
