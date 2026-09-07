import streamlit as st
from config import GROQ_API_KEY
from modules.pdf_parser import extract_text_from_pdf
from modules.rag_engine import build_vector_store, search_vector_store
from modules.db import insert_statement, insert_transactions
from modules.analytics import compute_analytics
from modules.dashboard import plot_balance_trend, plot_transaction_types, plot_debit_credit_comparison
from modules.extractor import extract_transactions, classify_transactions, clean_amounts

st.set_page_config(page_title="StatIQ", page_icon="🏦", layout="wide")

st.title("🏦 StatIQ — Bank Statement Analyzer")
st.markdown("*Automated credit analysis for NBFCs, CA firms & DSAs*")
st.divider()

uploaded_file = st.file_uploader("Upload bank statement (PDF)", type="pdf")

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        uploaded_file.seek(0)
        text = extract_text_from_pdf(uploaded_file)
    st.success(f"Extracted text — {len(text)} characters")

    with st.expander("View raw extracted text"):
        st.text(text)

    with st.spinner("Building vector store..."):
        vector_store = build_vector_store(text)
    st.success("Vector store built successfully")

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

        # Step 5 — Save to Supabase
        with st.spinner("Saving to database..."):
            statement_id = insert_statement(
                account_holder="Rahul Sharma",
                account_number="XXXX4821",
                bank_name="Axis Bank",
                ifsc_code="UTIB0001234",
                statement_period="01/03/2026 to 31/03/2026",
                opening_balance=24500.00,
                closing_balance=18320.00
            )
            insert_transactions(statement_id, df)
        st.success(f"✅ Saved to Supabase — Statement ID: {statement_id}")
                # Step 6 — Analytics
        st.divider()
        st.subheader("📈 Credit Analytics")
        analytics = compute_analytics(df)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Credits", f"₹{analytics['total_credits']:,.2f}")
        col2.metric("Total Debits", f"₹{analytics['total_debits']:,.2f}")
        col3.metric("Avg Balance", f"₹{analytics['avg_monthly_balance']:,.2f}")

        col4, col5, col6 = st.columns(3)
        col4.metric("Salary Credits", f"₹{analytics['salary_credits']:,.2f}")
        col5.metric("EMI Payments", f"₹{analytics['emi_payments']:,.2f}")
        col6.metric("EMI Ratio", f"{analytics['emi_ratio']}%")

        col7, col8 = st.columns(2)
        col7.metric("Bounce Count", analytics['bounce_count'])
        col8.metric("Balance Std Dev", f"₹{analytics['balance_std']:,.2f}")
                # Step 7 — Charts
        st.divider()
        st.subheader("📊 Visual Dashboard")

        col_left, col_right = st.columns(2)
        with col_left:
            st.plotly_chart(plot_balance_trend(df), use_container_width=True)
        with col_right:
            st.plotly_chart(plot_transaction_types(df), use_container_width=True)

        st.plotly_chart(plot_debit_credit_comparison(analytics), use_container_width=True)

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