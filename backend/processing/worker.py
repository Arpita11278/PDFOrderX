from backend.extraction.pdf_reader import PDFReader
from backend.extraction.ocr import OCREngine
from backend.extraction.customer_extractor import CustomerExtractor
from backend.extraction.order_extractor import OrderExtractor
from backend.extraction.awb_extractor import AWBExtractor
from backend.extraction.validator import Validator
from backend.utils.logger import logger

def process_single_page(file_path: str, page_num: int, use_ocr_fallback: bool = True) -> dict:
    try:
        raw_text = PDFReader.extract_page_text(file_path, page_num)
        
        if not raw_text.strip() and use_ocr_fallback:
            logger.info(f"Direct text extraction empty on page {page_num}. Triggering OCR fallback.")
            raw_text = OCREngine.extract_text_with_ocr(file_path, page_num)
            
        if not raw_text.strip():
            return {
                "page": page_num,
                "status": "FAILED",
                "confidence": 0,
                "confidence_reasons": ["Empty text extracted from page even after OCR"],
                "error_message": "Page contains no extractable text layer or image text"
            }
            
        name, name_reasons = CustomerExtractor.extract_customer_name(raw_text)
        address, address_reasons = CustomerExtractor.extract_customer_address(raw_text)
        order_id, order_reasons = OrderExtractor.extract_order_id(raw_text)
        awb, awb_reasons = AWBExtractor.extract_awb(raw_text)
        
        confidence, val_reasons, status = Validator.validate_and_score(name, address, order_id, awb)
        all_reasons = name_reasons + address_reasons + order_reasons + awb_reasons + val_reasons
        
        return {
            "page": page_num,
            "customer_name": name,
            "customer_address": address,
            "order_id": order_id,
            "awb_id": awb,
            "status": status,
            "confidence": confidence,
            "confidence_reasons": str(all_reasons),
            "error_message": None,
            "raw_text": raw_text
        }
    except Exception as e:
        logger.error(f"Error processing page {page_num}: {str(e)}")
        return {
            "page": page_num,
            "status": "FAILED",
            "confidence": 0,
            "confidence_reasons": [],
            "error_message": str(e)
        }