import pdfplumber
import pandas as pd
import re

DATE_RE = re.compile(r'^\d{2}/\d{2}/\d{2,4}')
AMOUNT_RE = re.compile(r'[\d,]+\.\d{2}')
CREDIT_KEYWORDS = re.compile(
    r'NEFT.*SALARY|SALARY|FREELANCE|CREDIT|CR\b|NEFTINW', 
    re.IGNORECASE
)

def extract_transactions(uploaded_file):
    """
    Extracts transactions by parsing raw text line by line.
    Uses regex to detect dates, amounts, and narration — robust against
    pdfplumber table-splitting issues.
    """
    rows = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split("\n"):
                line = line.strip()
                if not DATE_RE.match(line):
                    continue

                # Extract date — first 8 chars
                date = line[:8].strip()
                rest = line[8:].strip()

                # Find all amounts in line
                amounts = AMOUNT_RE.findall(rest)

                # Remove amounts from rest to isolate narration + ref
                narration_ref = AMOUNT_RE.sub("", rest).strip()
                parts = narration_ref.split()

                # Last token is ref no, rest is narration
                if len(parts) >= 2:
                    ref = parts[-1]
                    narration = " ".join(parts[:-1])
                else:
                    ref = "-"
                    narration = narration_ref

                # Determine credit vs debit by keyword
                is_credit = bool(CREDIT_KEYWORDS.search(narration))

                if len(amounts) == 1:
                    debit, credit, balance = "", "", amounts[0]
                elif len(amounts) == 2:
                    if is_credit:
                        debit, credit, balance = "", amounts[0], amounts[1]
                    else:
                        debit, credit, balance = amounts[0], "", amounts[1]
                elif len(amounts) == 3:
                    debit, credit, balance = amounts[0], amounts[1], amounts[2]
                else:
                    debit, credit, balance = "", "", ""

                rows.append([date, narration, ref, debit, credit, balance])

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows, columns=["Date", "Narration", "Ref No", "Debit", "Credit", "Balance"])
    df = df.dropna(how="all")
    return df


def classify_transactions(df):
    if df.empty or "Narration" not in df.columns:
        return df

    df = df.copy()
    df["Type"] = "Other"
    df.loc[df["Narration"].str.contains("SALARY|PAYROLL|SAL CR", case=False, na=False), "Type"] = "Salary"
    df.loc[df["Narration"].str.contains("ACHD|EMI|LOAN", case=False, na=False), "Type"] = "EMI"
    df.loc[df["Narration"].str.contains("BOUNCE|RETURN|DISHONOUR", case=False, na=False), "Type"] = "Bounce"
    df.loc[df["Narration"].str.contains("ATM|WDL", case=False, na=False), "Type"] = "ATM"
    df.loc[df["Narration"].str.contains("UPI", case=False, na=False), "Type"] = "UPI"
    df.loc[df["Narration"].str.contains("NEFT|IMPS|RTGS", case=False, na=False), "Type"] = "NEFT/IMPS"
    return df


def clean_amounts(df):
    for col in ["Debit", "Credit", "Balance"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "").str.strip(),
                errors="coerce"
            )
    return df