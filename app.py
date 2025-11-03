import streamlit as st
from dotenv import load_dotenv
import os

import logging
import sys
from pathlib import Path
from config.logging_config import setup_logging, get_logger
from config.settings import DEBUG, ENVIRONMENT

from src.llm import text2sql_chain
from src.sql import run_query

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="Text2SQL - Ask Database",
    page_icon="📚",
    layout="wide"
)

# -------------------- Load Env & Logging --------------------
load_dotenv()
if 'logger' not in st.session_state:
    log_level = "DEBUG" if DEBUG else "INFO"
    setup_logging(log_level=log_level)
    st.session_state.logging_initialized = True

    st.session_state.logger = get_logger(__name__)
    st.session_state.logger.info("Streamlit app started")

# -------------------- UI --------------------
st.title("📚 Text2SQL - Ask Database")
st.markdown("---")

# Initialize session state
if "count" not in st.session_state:
    st.session_state.count = 0
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# Input box for user query
user_query = st.text_input("💡 Ask your question:", placeholder="e.g., Count of all employees")

# Submit button
if st.button("🚀 Submit"):
    if user_query.strip() == "":
        st.warning("⚠️ Please enter a question before submitting.")
    else:
        if user_query.strip() != st.session_state.last_query:
            st.session_state.count += 1
            st.session_state.last_query = user_query.strip()
            st.session_state.last_result = text2sql_chain.invoke(st.session_state.last_query)
            st.session_state.logger.info('output displayed')
            test = run_query(st.session_state.last_result['sql_query'])
        
        else:
            st.info("Output not changed")
        
        # Show last stored result (whether new or same query)
        st.markdown(f"```sql\n{st.session_state.last_result['sql_query']}\n```")
        st.text(test)
