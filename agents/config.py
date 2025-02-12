import os
from dotenv import load_dotenv

load_dotenv()

GPT_API_KEY = None
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
DB_USERNAME = os.getenv("MONGO_DB_USERNAME", None)
DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD", None)
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("MONGO_DB_PORT")
WORK_DIR = os.getenv("WORK_DIR", "./work_dir")
REDIS_CHANEL = os.getenv("REDIS_CHANNEL", "messages")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
WIKIPEDIA_API_URL = os.getenv("WIKIPEDIA_API_URL", None)
OPERATION_SYSTEM = os.getenv("OPERATION_SYSTEM", "Ubuntu 22.04")
