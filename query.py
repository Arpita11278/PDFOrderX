import sqlite3
import pandas as pd

conn = sqlite3.connect('./data/database/extractor_metadata.db')
df = pd.read_sql_query("SELECT pdf_page, order_id, awb_id, customer_name FROM orders", conn)
print(df)
