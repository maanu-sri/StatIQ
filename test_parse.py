import streamlit as st
import pdfplumber

uploaded = st.file_uploader("Upload bank statement", type="pdf")

if uploaded:
    with pdfplumber.open(uploaded) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            st.write(text)