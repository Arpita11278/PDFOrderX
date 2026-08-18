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
            import fitz
            doc = fitz.open(file_path)
            if page_num < 0 or page_num >= len(doc):
                doc.close()
                return ""
            
            page = doc[page_num]
            words = page.get_text("words")
            doc.close()
            
            if not words:
                return ""
                
            # words format: (x0, y0, x1, y1, "word", block_no, line_no, word_no)
            # Group words by line (using y0 with a small tolerance)
            lines = {}
            for w in words:
                x0, y0, x1, y1, text = w[0], w[1], w[2], w[3], w[4]
                # Round y0 to nearest 5 to group words on the same line
                line_y = round(y0 / 5) * 5
                if line_y not in lines:
                    lines[line_y] = []
                lines[line_y].append((x0, text))
                
            # Sort lines top-to-bottom
            sorted_lines = sorted(lines.keys())
            
            extracted_text = []
            for line_y in sorted_lines:
                # Sort words in this line left-to-right
                line_words = sorted(lines[line_y], key=lambda item: item[0])
                line_text = " ".join([item[1] for item in line_words])
                extracted_text.append(line_text)
                
            return "\n".join(extracted_text)
        except Exception as e:
            from backend.utils.logger import logger
            logger.error(f"Error extracting text spatially: {str(e)}")
            return ""