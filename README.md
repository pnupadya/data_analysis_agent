# data_analysis_agent
AI agent which autonomously analysis data to identify root cause of an issue.

pip install langchain langchain-community psycopg2 pandas fastapi uvicorn requests pyyaml llama-cpp-python

curl "http://localhost:9000/weather?start_date=2024-07-01&end_date=2024-07-31&region=West"

[
    {
        "date": "2024-07-01",
        "region": "West",
        "temperature_c": 41.2,
        "rainfall_mm": 0.0
    },
    ...
]
cd /Users/pnupadya/Documents/learn/git_repos/data_analysis_agent
python weather_service.py
