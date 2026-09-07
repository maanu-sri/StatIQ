import plotly.express as px
import pandas as pd

def plot_balance_trend(df):
    fig = px.line(
        df, x="Date", y="Balance",
        title="Balance Trend Over Time",
        markers=True,
        color_discrete_sequence=["#00C897"]
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_transaction_types(df):
    type_counts = df["Type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    fig = px.bar(
        type_counts, x="Type", y="Count",
        title="Transaction Types Breakdown",
        color="Type",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    return fig

def plot_debit_credit_comparison(analytics):
    data = pd.DataFrame({
        "Category": ["Total Credits", "Total Debits", "Salary", "EMI"],
        "Amount": [
            analytics["total_credits"],
            analytics["total_debits"],
            analytics["salary_credits"],
            analytics["emi_payments"]
        ]
    })
    fig = px.bar(
        data, x="Category", y="Amount",
        title="Credits vs Debits Overview",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig