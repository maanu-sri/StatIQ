import streamlit as st
from config import GROQ_API_KEY

st.set_page_config(
    page_title="StatIQ",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 StatIQ — Bank Statement Analyzer")
st.markdown("*Automated credit analysis for NBFCs, CA firms & DSAs*")

st.divider()

st.info("Upload pipeline coming in Day 2. Environment is live ✅")

# Quick sanity check — never print real keys in production
if GROQ_API_KEY:
    st.success("Groq API key loaded successfully")
else:
    st.error("Groq API key missing — check your .env file")