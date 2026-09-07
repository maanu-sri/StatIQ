from groq import Groq
from config import GROQ_API_KEY
from modules.db import supabase

client = Groq(api_key=GROQ_API_KEY)

SCHEMA = """
Table: transactions
Columns: id, statement_id, date, narration, ref_no, debit, credit, balance, transaction_type

Table: statements  
Columns: id, account_holder, account_number, bank_name, statement_period, opening_balance, closing_balance
"""

def text_to_sql(question, statement_id):
    prompt = f"""
You are a SQL expert. Convert the user's question to a PostgreSQL query.
Only use SELECT statements. Never use DELETE, DROP, UPDATE or INSERT.
Always filter by statement_id = {statement_id}.

Schema:
{SCHEMA}

Question: {question}

Return ONLY the SQL query, nothing else. No explanation, no markdown, no backticks.
"""
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()


def run_nl_query(question, statement_id):
    sql = text_to_sql(question, statement_id)
    try:
        result = supabase.rpc("run_query", {"query": sql}).execute()
        return sql, result.data
    except Exception:
        # Direct table query fallback
        result = supabase.table("transactions")\
            .select("*")\
            .eq("statement_id", statement_id)\
            .execute()
        return sql, result.data