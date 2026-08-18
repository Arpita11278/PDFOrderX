import pandas as pd
from backend.database.db import get_db_connection

def generate_excel_export(path: str, status_filter: str = "All"):
    query = "SELECT pdf_page, customer_name, customer_address, order_id, awb_id, extraction_status, confidence, error_message FROM orders"
    params = ()
    if status_filter != "All":
        query += " WHERE extraction_status = ?"
        params = (status_filter,)
        
    with get_db_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params)
    
    df.to_excel(path, index=False)
    print(f"Generated excel export at {path}")
