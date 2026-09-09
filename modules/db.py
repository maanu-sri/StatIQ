from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import pandas as pd

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_statement(account_holder, account_number, bank_name, ifsc_code, statement_period, opening_balance, closing_balance):
    data = {"account_holder": account_holder, "account_number": account_number, "bank_name": bank_name, "ifsc_code": ifsc_code, "statement_period": statement_period, "opening_balance": opening_balance, "closing_balance": closing_balance}
    result = supabase.table("statements").insert(data).execute()
    return result.data[0]["id"]

def insert_transactions(statement_id, df):
    rows = []
    for _, row in df.iterrows():
        rows.append({"statement_id": statement_id, "date": str(row.get("Date","")), "narration": str(row.get("Narration","")), "ref_no": str(row.get("Ref No","")), "debit": float(row["Debit"]) if pd.notna(row.get("Debit")) else None, "credit": float(row["Credit"]) if pd.notna(row.get("Credit")) else None, "balance": float(row["Balance"]) if pd.notna(row.get("Balance")) else None, "transaction_type": str(row.get("Type","Other"))})
    result = supabase.table("transactions").insert(rows).execute()
    return len(result.data)

def fetch_transactions(statement_id):
    result = supabase.table("transactions").select("*").eq("statement_id", statement_id).execute()
    return pd.DataFrame(result.data)

def fetch_all_statements():
    result = supabase.table("statements").select("*").execute()
    return pd.DataFrame(result.data)
def log_event(event, statement_id=None, details=None):
    supabase.table("app_logs").insert({
        "event": event,
        "statement_id": statement_id,
        "details": details
    }).execute()