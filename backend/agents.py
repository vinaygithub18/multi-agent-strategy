import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from fpdf import FPDF
import google.generativeai as genai
from langgraph.graph import StateGraph, END
from typing import TypedDict

# ---------- TOOLS ----------
def scrape_market_news(query: str) -> str:
    """Scrapes latest market news headlines from Google News."""
    url = f"https://news.google.com/search?q={query}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    headlines = [a.text for a in soup.select("a.DY5T1d")]
    return "\n".join(headlines[:5]) if headlines else "No recent headlines found."

def load_market_data(topic: str) -> pd.DataFrame:
    """Simulates loading market data based on topic."""
    import random
    data = {
        "Month": ["Jan", "Feb", "Mar"],
        "Value": [random.randint(50, 100) for _ in range(3)]
    }
    return pd.DataFrame(data)

def generate_chart(df: pd.DataFrame, topic: str):
    """Generates a market trend chart and saves it."""
    plt.figure(figsize=(5,3))
    plt.plot(df["Month"], df["Value"], marker='o')
    plt.title(f"{topic} Market Trend")
    plt.ylabel("Market Value")
    plt.grid(True)
    plt.savefig("chart.png")
    plt.close()

def create_pdf_report(strategy_text: str):
    """Creates a PDF report containing the strategy and chart."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(0, 10, "Market Entry Strategy", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, strategy_text)
    pdf.image("chart.png", x=10, y=80, w=180)
    pdf.output("strategy_report.pdf")

# ---------- GEMINI ----------
def gemini_invoke(prompt: str) -> str:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# ---------- AGENTS ----------
def researcher_agent(state):
    topic = state["topic"]
    news = scrape_market_news(topic)
    return {"research_data": news}

def data_analyst_agent(state):
    topic = state["topic"]
    df = load_market_data(topic)
    generate_chart(df, topic)
    summary = f"{topic} market data:\n{df.to_string(index=False)}"
    return {"data_analysis": summary}

def strategy_agent(state):
    topic = state["topic"]
    research_data = state["research_data"]
    data_analysis = state["data_analysis"]

    prompt = f"""
    You are a market strategist.
    Topic: {topic}
    Research Data:
    {research_data}

    Data Analysis:
    {data_analysis}

    Create a clear, step-by-step market entry strategy for {topic}.
    """
    strategy_text = gemini_invoke(prompt)
    return {"strategy": strategy_text}

def presentation_agent(state):
    create_pdf_report(state["strategy"])
    return {"final_output": "strategy_report.pdf"}

# ---------- STATE SCHEMA ----------
class AgentState(TypedDict):
    topic: str
    research_data: str
    data_analysis: str
    strategy: str
    final_output: str

# ---------- WORKFLOW ----------
def run_multi_agent(topic: str):
    workflow = StateGraph(AgentState)

    workflow.add_node("Researcher", researcher_agent)
    workflow.add_node("DataAnalyst", data_analyst_agent)
    workflow.add_node("Strategist", strategy_agent)
    workflow.add_node("Presenter", presentation_agent)

    workflow.set_entry_point("Researcher")
    workflow.add_edge("Researcher", "DataAnalyst")
    workflow.add_edge("DataAnalyst", "Strategist")
    workflow.add_edge("Strategist", "Presenter")
    workflow.add_edge("Presenter", END)

    app = workflow.compile()
    return app.invoke({"topic": topic})
