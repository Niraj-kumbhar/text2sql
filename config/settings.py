import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data/input"
VECTOR_DB_DIR = BASE_DIR / "vector_db/faiss"
RAG_DIR = BASE_DIR / "rag"
TEST_OUTPUT_DIR = BASE_DIR/"tests/dummy_outputs"


# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE_MAX_SIZE = int(os.getenv("LOG_FILE_MAX_SIZE", "10485760"))  # 10MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# Application settings
DEBUG = False
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
TESTING = True

# RAG specific settings
EMBEDDING_MODEL = 'text-embedding-3-small'
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 100
COLLECTION_NAME = "mysql_employees_tables"

# LLM
MODEL = 'gpt-4.1-nano-2025-04-14'
