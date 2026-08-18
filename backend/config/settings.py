import os

WORKERS = 4
BATCH_SIZE = 100
OCR_FALLBACK = True
AUTO_SAVE = True
CHECKPOINT_INTERVAL = 100
CONFIDENCE_THRESHOLD = 80
OUTPUT_DIRECTORY = "./data/output"
DB_PATH = "./data/database/extractor_metadata.db"

os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs("logs", exist_ok=True)