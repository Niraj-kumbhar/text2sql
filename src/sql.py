from langchain_community.utilities.sql_database import SQLDatabase
import os
import logging


from config.logging_config import get_logger

_db_user = os.getenv('DB_USER')
_db_pass = os.getenv('DB_CRED')

logger = get_logger('src.sql')

def run_query(sql_query: str):
    """
    This Function will be deprecated in the future.
    """
    
    if not _db_user or not _db_pass:
        logger.error("Database credentials are missing.")
        raise ValueError("Database credentials are missing.")
    if not sql_query:
        logger.error("SQL query must not be empty.")
        raise ValueError("SQL query must not be empty.")

    DATABASE_URI = f"mysql+pymysql://{_db_user}:{_db_pass}@localhost:3306/employees"
    sql_database = None
    result = None

    try:
        sql_database = SQLDatabase.from_uri(DATABASE_URI)
        result = sql_database.run(sql_query)
        logger.info('data fetched successfully')
        return result
    except Exception as e:
        logger.error(f"Error running query: {e}")
        raise

import pandas as pd
from sqlalchemy import create_engine
import os

def run_query_df(sql_query: str):
    _db_user = os.getenv('DB_USER')
    _db_pass = os.getenv('DB_CRED')

    if not _db_user or not _db_pass:
        raise ValueError("Database credentials are missing.")
    if not sql_query:
        raise ValueError("SQL query must not be empty.")

    DATABASE_URI = f"mysql+pymysql://{_db_user}:{_db_pass}@localhost:3306/employees"

    engine = create_engine(DATABASE_URI)
    df = pd.read_sql(sql_query, engine)

    return df


