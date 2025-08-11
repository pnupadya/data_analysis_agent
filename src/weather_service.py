from flask import Flask, jsonify, request
import pandas as pd
from datetime import datetime

# Path to your weather CSV
WEATHER_CSV_PATH = "data/weather.csv"

# Load the CSV
df_weather = pd.read_csv(WEATHER_CSV_PATH, parse_dates=["date"])

app = Flask(__name__)

@app.route("/weather", methods=["GET"])
def get_weather():
    """
    Query parameters:
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
        region: e.g., "West"
    """
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    region = request.args.get("region")

    # Validate params
    if not all([start_date, end_date, region]):
        return jsonify({"error": "Missing parameters. Required: start_date, end_date, region"}), 400

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format, should be YYYY-MM-DD"}), 400

    # Filter data
    mask = (df_weather["date"] >= start) & (df_weather["date"] <= end) & (df_weather["region"] == region)
    result_df = df_weather.loc[mask]

    # Convert to list of dicts
    data = result_df.to_dict(orient="records")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
