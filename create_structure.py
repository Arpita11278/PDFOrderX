import os

structure = [
    "backend/config",
    "backend/database",
    "backend/extraction",
    "backend/processing",
    "backend/exports",
    "backend/models",
    "backend/utils",
    "frontend/components",
    "frontend/assets/icons",
    "tests",
    "data/input",
    "data/output",
    "data/database",
    "logs",
    "config"
]

files = [
    "backend/main.py",
    "backend/config/settings.py",
    "backend/database/db.py",
    "backend/database/models.py",
    "backend/extraction/pdf_reader.py",
    "backend/extraction/customer_extractor.py",
    "backend/extraction/order_extractor.py",
    "backend/extraction/awb_extractor.py",
    "backend/extraction/ocr.py",
    "backend/extraction/validator.py",
    "backend/processing/worker.py",
    "backend/processing/batch_processor.py",
    "backend/processing/checkpoint.py",
    "backend/processing/progress.py",
    "backend/processing/error_handler.py",
    "backend/exports/excel.py",
    "backend/exports/csv.py",
    "backend/models/schemas.py",
    "backend/utils/logger.py",
    "backend/utils/file_utils.py",
    "backend/utils/helpers.py",
    "frontend/main_window.py",
    "frontend/components/file_selector.py",
    "frontend/components/progress_bar.py",
    "frontend/components/results_table.py",
    "frontend/components/search_bar.py",
    "tests/test_customer_extractor.py",
    "tests/test_order_extractor.py",
    "tests/test_awb_extractor.py",
    "tests/test_validator.py",
    "tests/test_checkpoint.py",
    "logs/.gitkeep",
    "config/config.json",
    "requirements.txt",
    ".gitignore",
    ".env.example",
    "README.md",
    "run.py"
]

for folder in structure:
    os.makedirs(folder, exist_ok=True)

for file in files:
    if not os.path.exists(file):
        with open(file, "w") as f:
            pass

print("Project structure successfully created!")
