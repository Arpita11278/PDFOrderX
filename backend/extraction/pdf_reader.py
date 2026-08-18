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
            doc = fitz.open(file_path)
            if page_num < 0 or page_num >= len(doc):
                doc.close()
                return ""
                
            page = doc[page_num]
            # Use "words" instead of "text" to avoid words squishing together when spaces are missing in PDF
            words = page.get_text("words")
            if words:
                text = " ".join([w[4] for w in words])
            else:
                text = page.get_text("text")
            doc.close()
            return text
        except Exception as e:
            logger.error(f"Error extracting text from page {page_num} of {file_path}: {str(e)}")
            return ""