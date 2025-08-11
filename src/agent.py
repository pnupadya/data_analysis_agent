import os
from langchain.llms import LlamaCpp
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from tools import (
    load_config,
    fetch_postgres_table,
    load_csv,
    load_weather_from_api,
    generate_html_report_tool
)

CONFIG_PATH = "/Users/pnupadya/Documents/learn/git_repos/data_analysis_agent/config.yaml"

def main():
    # Load config
    config = load_config(CONFIG_PATH)

    # Setup LLM
    llm = LlamaCpp(
        model_path=config["llm"]["model_path"],
        temperature=config["llm"]["temperature"],
        max_tokens=config["llm"]["max_tokens"],
        verbose=True
    )

    # Define tools
    def get_sales_data(_):
        return fetch_postgres_table(config, "sales").to_csv(index=False)

    def get_inventory_data(_):
        return fetch_postgres_table(config, "inventory").to_csv(index=False)

    def get_marketing_data(_):
        return load_csv(config["paths"]["marketing_csv"]).to_csv(index=False)

    def get_weather_data(_):
        return load_weather_from_api(config["weather_api"]["url"]).to_csv(index=False)

    tools = [
        Tool(name="Sales Data", func=get_sales_data, description="Get sales data as CSV string"),
        Tool(name="Inventory Data", func=get_inventory_data, description="Get inventory data as CSV string"),
        Tool(name="Marketing Data", func=get_marketing_data, description="Get marketing data as CSV string"),
        Tool(name="Weather Data", func=get_weather_data, description="Get weather data as CSV string")
    ]

    # Initialize agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Ask the agent to analyze
    analysis_prompt = """
    You are a data analyst. Use all the provided tools to fetch and analyze sales, inventory, marketing, and weather data.
    Find possible causes for anomalies in sales patterns.
    Provide a concise final analysis.
    """
    final_analysis = agent.run(analysis_prompt)

    # Generate HTML report automatically
    dfs = {
        "sales": fetch_postgres_table(config, "sales"),
        "inventory": fetch_postgres_table(config, "inventory"),
        "marketing": load_csv(config["paths"]["marketing_csv"]),
        "weather": load_weather_from_api(config["weather_api"]["url"])
    }
    generate_html_report_tool(final_analysis, dfs, config["paths"]["report_html"])

if __name__ == "__main__":
    main()
