import fitz  # PyMuPDF
from backend.utils.logger import logger

class PDFReader:
    @staticmethod
    def analyze_pdf(file_path: str) -> dict:
        """Analyzes a PDF file and returns basic metadata including page count and file size."""
        try:
            doc = fitz.open(file_path)
            page_count = len(doc)
            doc.close()
            
            import os
            file_size = os.path.getsize(file_path)
            
            logger.info(f"PDF analyzed successfully: {file_path}, Pages: {page_count}")
            return {
                "file_path": file_path,
                "file_size": file_size,
                "page_count": page_count
            }
        except Exception as e:
            logger.error(f"Error analyzing PDF {file_path}: {str(e)}")
            raise e

    @staticmethod
    def extract_page_text(file_path: str, page_num: int) -> str:
        """Extracts plain text layer from a specific page of a PDF."""
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                if page_num < 0 or page_num >= len(pdf.pages):
                    return ""
                
                page = pdf.pages[page_num]
                # x_tolerance and y_tolerance help in adding spaces where they logically belong
                text = page.extract_text(x_tolerance=2, y_tolerance=2)
                return text if text else ""
        except Exception as e:
            logger.error(f"Error extracting text from page {page_num} of {file_path} with pdfplumber: {str(e)}")
            return ""