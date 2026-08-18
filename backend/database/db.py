import sqlite3
from contextlib import contextmanager
from backend.config.settings import DB_PATH
from backend.database.models import CREATE_PROJECTS_TABLE, CREATE_ORDERS_TABLE

def init_db():
    """Initializes the SQLite database and creates required tables and indexes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(CREATE_PROJECTS_TABLE)
    cursor.execute(CREATE_ORDERS_TABLE)
    
    # Create indexes for performance optimization
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_id ON orders(order_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_awb_id ON orders(awb_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pdf_page ON orders(pdf_page)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON orders(extraction_status)")
    
    conn.commit()
    conn.close()

@contextmanager
def get_db_connection():
    """Context manager for safe database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()