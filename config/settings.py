import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
_BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = _BASE_DIR / "config"
LOGS_DIR = _BASE_DIR / "logs"
INPUT_DATA_TABLES_DIR = _BASE_DIR / "data/tables"
INPUT_DATA_SAMPLE_DIR = _BASE_DIR / "data/sample_queries"
VECTOR_DB_DIR_TABLES = _BASE_DIR / "vector_db/TABLES"
VECTOR_DB_DIR_SAMPLEQ = _BASE_DIR / "vector_db/SAMPLEQ_DB"
RAG_DIR = _BASE_DIR / "rag"
TEST_OUTPUT_DIR = _BASE_DIR/"tests/dummy_outputs"


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
