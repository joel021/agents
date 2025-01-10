import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)
GPT_API_KEY = os.getenv("GPT_API_KEY", None)
DB_USERNAME = os.getenv("DB_USERNAME", None)
DB_PASSWORD = os.getenv("DB_PASSWORD", None)
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
WORK_DIR = os.getenv("WORK_DIR", "")
SINGLE_AGENTS = os.getenv("SINGLE_AGENTS", True)
