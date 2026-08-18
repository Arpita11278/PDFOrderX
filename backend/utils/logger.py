import logging
import os

os.makedirs("logs", exist_ok=True)

def setup_logger(name: str, log_file: str = "logs/application.log"):
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(logging.INFO)
    
    if not logger_instance.handlers:
        # File Handler
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.INFO)
        
        # Console Handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger_instance.addHandler(fh)
        logger_instance.addHandler(ch)
        
    return logger_instance

# Global logger object export taaki baaki files `from backend.utils.logger import logger` kar sakein
logger = setup_logger("PDFExtractor")