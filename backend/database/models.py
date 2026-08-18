CREATE_PROJECTS_TABLE = """
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT,
    pdf_filename TEXT,
    pdf_size INTEGER,
    page_count INTEGER,
    processing_status TEXT,
    processed_pages INTEGER,
    last_checkpoint INTEGER,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pdf_page INTEGER UNIQUE,
    customer_name TEXT,
    customer_address TEXT,
    order_id TEXT,
    awb_id TEXT,
    extraction_status TEXT,
    confidence INTEGER,
    confidence_reasons TEXT,
    error_message TEXT,
    raw_text TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""