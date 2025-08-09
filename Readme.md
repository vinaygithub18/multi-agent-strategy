# 📊 Multi-Agent Market Strategy AI

> **Live Demo:** [Streamlit App](https://your-live-demo-link.streamlit.app)  
> **Author:** Your Name | **Experience:** 2 years Software Engineer | **Focus:** Agentic AI Applications

An **autonomous multi-agent system** that uses **Gemini LLMs** to research, analyze data, and create **professional market entry strategy reports** — complete with charts and downloadable PDFs.

---

## 🚀 Features

- **Multi-Agent Workflow**  
  - Researcher → Data Analyst → Strategist → Presenter  
  - Fully orchestrated via [LangGraph](https://github.com/langchain-ai/langgraph)
- **Web Scraping** for recent market news
- **Data Analysis & Charting** with `pandas` & `matplotlib`
- **AI-Generated Strategy** using Google **Gemini API**
- **Instant PDF Reports** ready for sharing
- **One-Click Deployment** via Streamlit Cloud

---

## 🖼️ Demo Preview

![App Screenshot](samples/app_screenshot.png)

Sample generated PDF: [View Example](samples/sample_strategy_report.pdf)

---

## 🧠 How It Works

```mermaid
flowchart LR
    A[User Prompt] --> B[Researcher Agent]
    B --> C[Data Analyst Agent]
    C --> D[Strategy Agent]
    D --> E[Presentation Agent]
    E --> F[Download PDF]
