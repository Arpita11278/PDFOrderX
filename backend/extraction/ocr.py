import pymupdf
import pytesseract
from PIL import Image
import io
from backend.utils.logger import logger

class OCREngine:
    @staticmethod
    def extract_text_with_ocr(file_path: str, page_num: int) -> str:
        """Extracts text from a PDF page using Tesseract OCR by rendering the page as an image."""
        try:
            doc = pymupdf.open(file_path)
            if page_num < 0 or page_num >= len(doc):
                doc.close()
                return ""
                
            page = doc[page_num]
            # Render page to image (zoom factor 2 for better OCR clarity)
            pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
            img_data = pix.tobytes("png")
            doc.close()
            
            image = Image.open(io.BytesIO(img_data))
            text = pytesseract.image_to_string(image)
            
            logger.info(f"OCR successfully executed on page {page_num}")
            return text
        except Exception as e:
            logger.error(f"OCR execution failed on page {page_num} of {file_path}: {str(e)}")
            return ""