import os
from dotenv import load_dotenv

load_dotenv()

DB_DRIVER = os.getenv("DB_DRIVER")
DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

TESSERACT_CMD = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")
CONTINUITY_THRESHOLD = 0.85
POPPLER_PATH = os.getenv("POPPLER_PATH")
