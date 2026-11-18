
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Set to true to use demo data instead of calling Gemini.
USE_MOCK_VISION = os.getenv("USE_MOCK_VISION", "false").lower() == "true"

MAX_IMAGE_BYTES = 5 * 1024 * 1024
SERPAPI_KEY = os.getenv("SERPAPI_KEY")