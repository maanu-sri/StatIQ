import streamlit as st
from config import GROQ_API_KEY
from modules.pdf_parser import extract_text_from_pdf
from modules.rag_engine import build_vector_store, search_vector_store
from modules.extractor import extract_transactions, classify_transactions, clean_amounts

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
    # Step 1 — Raw text
    with st.spinner("Extracting text from PDF..."):
        uploaded_file.seek(0)
        text = extract_text_from_pdf(uploaded_file)
    st.success(f"Extracted text — {len(text)} characters")

    with st.expander("View raw extracted text"):
        st.text(text)

    # Step 2 — RAG
    with st.spinner("Building vector store..."):
        vector_store = build_vector_store(text)
    st.success("Vector store built successfully")

    # Step 3 — Transactions
    st.divider()
    st.subheader("📊 Transaction Data")

    with st.spinner("Extracting transactions..."):
        uploaded_file.seek(0)
        df = extract_transactions(uploaded_file)
        df = classify_transactions(df)
        df = clean_amounts(df)

    if df.empty:
        st.warning("No transactions found")
    else:
        st.success(f"Extracted {len(df)} transactions")
        st.write("**Transaction Types Found:**")
        st.dataframe(df["Type"].value_counts().reset_index())
        with st.expander("View all transactions"):
            st.dataframe(df)

    # Step 4 — Query
    st.divider()
    query = st.text_input("Ask a question about this bank statement:")
    if query:
        results = search_vector_store(query, vector_store)
        st.subheader("Relevant chunks found:")
        for i, result in enumerate(results):
            st.write(f"Chunk {i+1}:")
            st.info(result.page_content)

else:
    st.info("Upload a bank statement PDF to begin analysis")