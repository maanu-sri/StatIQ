import pandas as pd

def compute_analytics(df):
    """
    Computes key credit risk metrics from transaction DataFrame.
    Returns a dict of analytics.
    """
    analytics = {}

    # Total credits and debits
    analytics["total_credits"] = df["Credit"].sum()
    analytics["total_debits"] = df["Debit"].sum()

    # Salary credits
    salary_df = df[df["Type"] == "Salary"]
    analytics["salary_credits"] = salary_df["Credit"].sum()
    analytics["salary_count"] = len(salary_df)

    # EMI payments
    emi_df = df[df["Type"] == "EMI"]
    analytics["emi_payments"] = emi_df["Debit"].sum()
    analytics["emi_count"] = len(emi_df)

    # Bounce count
    analytics["bounce_count"] = len(df[df["Type"] == "Bounce"])

    # Average monthly balance
    balance_series = df["Balance"].dropna()
    analytics["avg_monthly_balance"] = round(balance_series.mean(), 2)
    analytics["min_balance"] = balance_series.min()
    analytics["max_balance"] = balance_series.max()

    # EMI obligation ratio — EMI as % of salary
    if analytics["salary_credits"] > 0:
        analytics["emi_ratio"] = round((analytics["emi_payments"] / analytics["salary_credits"]) * 100, 2)
    else:
        analytics["emi_ratio"] = 0

    # Income stability — std deviation of balance (lower = more stable)
    analytics["balance_std"] = round(balance_series.std(), 2)

    return analytics