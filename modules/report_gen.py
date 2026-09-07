from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_risk_report(analytics, anomaly_df, account_holder="Rahul Sharma"):
    """
    Generates a structured creditworthiness report using LLaMA 3.3 70B.
    """
    # Build anomaly summary
    if anomaly_df.empty:
        anomaly_summary = "No anomalies detected."
    else:
        anomaly_summary = "\n".join([
            f"- {row['Flag']}: {row['Narration']} (Amount: {row['Amount']})"
            for _, row in anomaly_df.iterrows()
        ])

    prompt = f"""
You are a senior credit analyst at an NBFC in India. Based on the following bank statement analytics, write a structured creditworthiness assessment report.

Account Holder: {account_holder}

FINANCIAL METRICS:
- Total Credits: ₹{analytics['total_credits']:,.2f}
- Total Debits: ₹{analytics['total_debits']:,.2f}
- Salary Credits: ₹{analytics['salary_credits']:,.2f}
- EMI Payments: ₹{analytics['emi_payments']:,.2f}
- EMI Obligation Ratio: {analytics['emi_ratio']}%
- Average Monthly Balance: ₹{analytics['avg_monthly_balance']:,.2f}
- Minimum Balance: ₹{analytics['min_balance']:,.2f}
- Balance Std Deviation: ₹{analytics['balance_std']:,.2f}
- Bounce Count: {analytics['bounce_count']}

RISK FLAGS:
{anomaly_summary}

Write the report in the following format:
1. EXECUTIVE SUMMARY (2-3 sentences)
2. INCOME ASSESSMENT
3. DEBT OBLIGATION ANALYSIS
4. RISK INDICATORS
5. CREDITWORTHINESS VERDICT (Approve / Conditional Approve / Reject with reason)

Be specific, use the numbers provided, and write in plain English suitable for a loan officer.
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    return response.choices[0].message.content