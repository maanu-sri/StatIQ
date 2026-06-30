import pdfplumber

def extract_text_from_pdf(uploaded_file):
    """
    Extracts raw text from all pages of an uploaded bank statement PDF.
    Returns a single combined string of all page text.
    """
    full_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text


def extract_tables_from_pdf(uploaded_file):
    """
    Extracts tables from all pages of an uploaded bank statement PDF.
    Returns a list of tables, where each table is a list of rows.
    """
    all_tables = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                all_tables.append(table)
    return all_tables