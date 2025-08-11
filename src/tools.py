import pandas as pd
import psycopg2
import requests
import matplotlib.pyplot as plt
from jinja2 import Template
import os
import yaml

# Load config
def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# Postgres connection
def fetch_postgres_table(config, table_name):
    conn = psycopg2.connect(
        host=config["database"]["host"],
        port=config["database"]["port"],
        dbname=config["database"]["dbname"],
        user=config["database"]["user"],
        password=config["database"]["password"]
    )
    query = f'SELECT * FROM {config["database"]["schema"]}.{table_name}'
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# CSV loader
def load_csv(path):
    return pd.read_csv(path)

# Weather API (from CSV served as API)
def load_weather_from_api(api_url):
    resp = requests.get(api_url)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())

def fetch_weather_data(api_url, start_date, end_date, region):
    """
    Call the weather API and return pandas DataFrame.
    """
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "region": region
    }
    response = requests.get(api_url, params=params)

    if response.status_code != 200:
        raise Exception(f"Weather API Error {response.status_code}: {response.text}")

    data = response.json()
    return pd.DataFrame(data)

# HTML report generator
def generate_html_report_tool(analysis_text, dfs, output_path):
    graphs = []
    for name, df in dfs.items():
        plt.figure(figsize=(6,4))
        df.plot(x=df.columns[0], y=df.columns[-1])
        img_path = f"{os.path.splitext(output_path)[0]}_{name}.png"
        plt.savefig(img_path)
        plt.close()
        graphs.append({"name": name, "path": os.path.basename(img_path)})

    html_template = """
    <html>
    <head><title>Analysis Report</title></head>
    <body>
    <h1>Data Analytics Report</h1>
    <h2>Final Analysis</h2>
    <p>{{ analysis_text }}</p>
    {% for g in graphs %}
        <h3>{{ g.name }}</h3>
        <img src="{{ g.path }}" width="600"><br>
    {% endfor %}
    </body>
    </html>
    """
    template = Template(html_template)
    html_content = template.render(analysis_text=analysis_text, graphs=graphs)

    with open(output_path, "w") as f:
        f.write(html_content)

    print(f"✅ HTML report generated: {output_path}")
