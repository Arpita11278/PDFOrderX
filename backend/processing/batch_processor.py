from backend.processing.worker import process_single_page
from backend.database.db import get_db_connection
import concurrent.futures

class BatchProcessor:
    @staticmethod
    def process_pdf_in_batches(project_id: int, file_path: str, total_pages: int, batch_size: int, max_workers: int):
        print(f"Starting batch processing for {file_path}, total pages: {total_pages}")
        
        results = []
        # Process pages in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Note: PyMuPDF/fitz is 0-indexed, so we pass 0 to total_pages-1
            future_to_page = {executor.submit(process_single_page, file_path, i): i for i in range(total_pages)}
            for future in concurrent.futures.as_completed(future_to_page):
                page_result = future.result()
                results.append(page_result)
        
        # Save to database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Clear previous orders so new PDF doesn't mix with old data
            cursor.execute("DELETE FROM orders")
            
            for r in results:
                cursor.execute("""
                    INSERT INTO orders (
                        pdf_page, customer_name, customer_address, order_id, awb_id, 
                        extraction_status, confidence, confidence_reasons, error_message, raw_text
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r.get("page"), r.get("customer_name"), r.get("customer_address"), 
                    r.get("order_id"), r.get("awb_id"), r.get("status"), 
                    r.get("confidence"), str(r.get("confidence_reasons")), 
                    r.get("error_message"), r.get("raw_text", "")
                ))
            
            # Update project status
            cursor.execute("UPDATE projects SET processing_status = 'COMPLETED', processed_pages = ? WHERE id = ?", (total_pages, project_id))
            conn.commit()
            
        print("Batch processing completed and saved to database.")
