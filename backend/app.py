import os
import streamlit as st
from agents import run_multi_agent

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Multi-Agent Market Strategy AI", page_icon="📊")

# --- GOOGLE API KEY ---
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

st.title("📊 Multi-Agent Market Strategy AI")
st.write("Generate a professional market entry strategy with autonomous AI agents.")

topic = st.text_input("Enter market/topic:", placeholder="e.g. Renewable energy India")

if st.button("Generate Strategy") and topic:
    with st.spinner("🤖 Running multi-agent workflow..."):
        run_multi_agent(topic)
    st.success("✅ Report generated successfully!")
    with open("strategy_report.pdf", "rb") as f:
        st.download_button("📥 Download PDF Report", f, file_name="strategy_report.pdf")
