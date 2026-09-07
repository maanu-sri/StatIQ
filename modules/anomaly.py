import pandas as pd

def detect_anomalies(df):
    """
    Detects suspicious patterns in transaction data.
    Returns a list of flagged transactions with reasons.
    """
    flags = []

    # 1 — Large cash withdrawals (ATM > 10000)
    atm_df = df[(df["Type"] == "ATM") & (df["Debit"] > 10000)]
    for _, row in atm_df.iterrows():
        flags.append({"Date": row["Date"], "Narration": row["Narration"], "Amount": row["Debit"], "Flag": "Large ATM Withdrawal"})

    # 2 — Bounce transactions
    bounce_df = df[df["Type"] == "Bounce"]
    for _, row in bounce_df.iterrows():
        flags.append({"Date": row["Date"], "Narration": row["Narration"], "Amount": row["Debit"], "Flag": "Cheque Bounce"})

    # 3 — Unusually large debits (> 2x average debit)
    avg_debit = df["Debit"].mean()
    large_debits = df[(df["Debit"] > 2 * avg_debit) & (df["Type"] != "Salary")]
    for _, row in large_debits.iterrows():
        flags.append({"Date": row["Date"], "Narration": row["Narration"], "Amount": row["Debit"], "Flag": "Unusually Large Debit"})

    # 4 — High EMI ratio warning
    salary = df[df["Type"] == "Salary"]["Credit"].sum()
    emi = df[df["Type"] == "EMI"]["Debit"].sum()
    if salary > 0 and (emi / salary) > 0.5:
        flags.append({"Date": "-", "Narration": "EMI burden exceeds 50% of salary", "Amount": emi, "Flag": "High EMI Ratio"})

    # 5 — No salary credit detected
    if df[df["Type"] == "Salary"].empty:
        flags.append({"Date": "-", "Narration": "No salary credit found in statement", "Amount": 0, "Flag": "No Salary Detected"})

    return pd.DataFrame(flags) if flags else pd.DataFrame()