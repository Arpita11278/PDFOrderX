from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from backend.database.db import init_db, get_db_connection
from backend.extraction.pdf_reader import PDFReader
from backend.processing.worker import process_single_page
from backend.processing.batch_processor import BatchProcessor
from backend.exports.excel import generate_excel_export
from backend.exports.csv import generate_csv_export
import os

# Yahan 'app' object define hona zaroori hai jise uvicorn load karta hai
app = FastAPI(title="Large PDF Order & AWB Extractor", version="1.0.0")

class ProjectInitRequest(BaseModel):
    file_path: str
    project_name: str

class ExtractionRunRequest(BaseModel):
    project_id: int
    file_path: str
    batch_size: int = 100
    workers: int = 4

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/api/project/init")
def initialize_project(payload: ProjectInitRequest):
    try:
        analysis = PDFReader.analyze_pdf(payload.file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projects (project_name, pdf_filename, pdf_size, page_count, processing_status, processed_pages, last_checkpoint)
            VALUES (?, ?, ?, ?, 'INITIALIZED', 0, 0)
        """, (payload.project_name, payload.file_path, analysis["file_size"], analysis["page_count"]))
        project_id = cursor.lastrowid
        conn.commit()
        
    return {"project_id": project_id, "message": "Project initialized successfully", "analysis": analysis}

@app.get("/api/test/sample")
def test_sample_page(file_path: str, page_num: int = 0):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    result = process_single_page(file_path, page_num)
    return result

@app.post("/api/extraction/start")
def start_extraction(payload: ExtractionRunRequest, background_tasks: BackgroundTasks):
    analysis = PDFReader.analyze_pdf(payload.file_path)
    total_pages = analysis["page_count"]
    
    background_tasks.add_task(
        BatchProcessor.process_pdf_in_batches,
        project_id=payload.project_id,
        file_path=payload.file_path,
        total_pages=total_pages,
        batch_size=payload.batch_size,
        max_workers=payload.workers
    )
    return {"message": "Extraction started in background", "total_pages": total_pages}

@app.get("/api/export/excel")
def export_excel(status: str = "All"):
    path = "./data/output/extracted_orders.xlsx"
    try:
        generate_excel_export(path, status_filter=status)
        return {"message": "Excel export generated successfully", "path": path}
    except PermissionError:
        raise HTTPException(status_code=400, detail="Permission Denied. Please close the Excel file 'extracted_orders.xlsx' if it is open in another program, and try again.")

@app.get("/api/export/csv")
def export_csv(status: str = "All"):
    path = "./data/output/extracted_orders.csv"
    try:
        generate_csv_export(path, status_filter=status)
        return {"message": "CSV export generated successfully", "path": path}
    except PermissionError:
        raise HTTPException(status_code=400, detail="Permission Denied. Please close the CSV file if it is open, and try again.")