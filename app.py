import streamlit as st
from config import GROQ_API_KEY
from modules.pdf_parser import extract_text_from_pdf, extract_tables_from_pdf

st.set_page_config(
    page_title="StatIQ",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 StatIQ — Bank Statement Analyzer")
st.markdown("*Automated credit analysis for NBFCs, CA firms & DSAs*")
st.divider()

uploaded_file = st.file_uploader("Upload bank statement (PDF)", type="pdf")

if uploaded_file:
    with st.spinner("Extracting data from PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        tables = extract_tables_from_pdf(uploaded_file)

    st.success(f"Extracted text from PDF — {len(text)} characters")
    st.success(f"Found {len(tables)} table(s) in PDF")

    with st.expander("View raw extracted text"):
        st.text(text)

    if tables:
        with st.expander("View extracted tables"):
            for i, table in enumerate(tables):
                st.write(f"Table {i+1}")
                st.dataframe(table)
else:
    st.info("Upload a bank statement PDF to begin analysis")