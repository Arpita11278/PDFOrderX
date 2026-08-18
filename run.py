import uvicorn
import os
from backend.database.db import init_db

def main():
    # Initialize database tables on startup
    init_db()
    print("Database initialized successfully.")
    
    print("Starting Large PDF Order & AWB Extractor server...")
    # Run FastAPI server using Uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()