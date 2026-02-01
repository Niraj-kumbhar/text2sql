import streamlit as st
import json
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage

from src.agents import agent_app as agent
from src.sql import run_query_df
from src.utils import tool_messages_to_documents_json

# Set page config
st.set_page_config(page_title="Text2SQL App", layout="centered")

with st.sidebar:
    database = st.selectbox("Explore Database",("employees"))

    st.markdown("## About")
    st.markdown(
        """
        This app allows you to interact with a Text2SQL agent that can generate SQL queries based on your natural language questions.
        
        **How to use:**
        1. Enter your question in the input box.
        2. Click the "Send" button.
        3. View the generated SQL query and results below.
        
        **Note:** Ensure your database is properly configured for accurate results.
        """
    )

# Custom CSS for centering and word wrap
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    h1 {
        text-align: center;
        margin-bottom: 3rem;
    }
    .stCodeBlock {
        word-wrap: break-word;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Text2SQL App")

# Initialize session state
if 'response' not in st.session_state:
    st.session_state.response = None
if 'df_result' not in st.session_state:
    st.session_state.df_result = None

# Add vertical spacing before input when no results
if st.session_state.response is None:
    st.markdown("<br>" * 8, unsafe_allow_html=True)

# Center input box and button
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    user_question = st.text_input(
        "Ask your question",
        placeholder="e.g., Show me all female employees with surname Baaz",
        label_visibility="collapsed"
    )
    
    send_button = st.button("Send", width='stretch', type="primary")

# Process when send button is clicked
if send_button and user_question:
    st.session_state.response = None
    st.session_state.df_result = None
    st.session_state.retrieved_docs = None
    
    # Show loading spinner while agent is processing
    with st.spinner("Processing your question..."):

        response = agent.invoke({"messages": [HumanMessage(content=user_question)]})
#         response = {'messages': [HumanMessage(content='list all tables in the database', additional_kwargs={}, response_metadata={}),
#   AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 23, 'prompt_tokens': 347, 'total_tokens': 370, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4.1-nano-2025-04-14', 'system_fingerprint': 'fp_93ba275753', 'id': 'chatcmpl-D4SJQmsRekLeIhItE2b8cB4EkzeLd', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--019c1982-9681-7e20-8e7b-4c9a8fb4e94f-0', tool_calls=[{'name': 'combined_retriever', 'args': {'user_query': 'list all tables in the database'}, 'id': 'call_j7WbAGi0MnVyVKcERuuVVEDG', 'type': 'tool_call'}], usage_metadata={'input_tokens': 347, 'output_tokens': 23, 'total_tokens': 370, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}),
#   ToolMessage(content='[Document(id=\'431703e5-c48c-4ede-bc27-9ca290002a3d\', metadata={\'source\': \'d:\\\\code\\\\text2sql\\\\data\\\\tables\\\\department.md\', \'table_name\': \'department\', \'token_count\': 54, \'index\': 101, \'type\': \'tables-info\'}, page_content=\'## Table Name: `departments`\\n\\n- **Description**: Lists all departments within the organization.\\n- **Primary Key**: `dept_no`\\n\\n### Columns:\\n- `dept_no`: Unique identifier for each department.\\n- `dept_name`: Name of the department.\'), Document(id=\'8f35b281-22d9-4fa3-b1b9-b29fca92094f\', metadata={\'sql\': "SELECT \\n    d.dept_name, \\n    e.first_name, \\n    e.last_name\\nFROM dept_manager dm\\nJOIN departments d ON dm.dept_no = d.dept_no\\nJOIN employees e ON dm.emp_no = e.emp_no\\nWHERE dm.to_date = \'9999-01-01\';", \'source\': \'queries.json\', \'index\': 3, \'type\': \'sample-queries\', \'token_count\': 10}, page_content=\'Get the list of department managers and their departments.\'), Document(id=\'d828f4c5-9ad7-486a-8a3d-21efedb09409\', metadata={\'source\': \'d:\\\\code\\\\text2sql\\\\data\\\\tables\\\\employees.md\', \'table_name\': \'employees\', \'token_count\': 95, \'index\': 104, \'type\': \'tables-info\'}, page_content="## Table Name: `employees`\\n\\n- **Description**: Contains personal information about each employee.\\n- **Primary Key**: `emp_no`\\n\\n### Columns:\\n- `emp_no`: Unique identifier for each employee.\\n- `birth_date`: Employee\'s date of birth.\\n- `first_name`: Employee\'s first name.\\n- `last_name`: Employee\'s last name.\\n- `gender`: Gender of the employee.\\n- `hire_date`: Date when the employee was hired."), Document(id=\'7817d430-70f6-453e-8f92-c3bda2f254fd\', metadata={\'source\': \'d:\\\\code\\\\text2sql\\\\data\\\\tables\\\\titles.md\', \'table_name\': \'titles\', \'token_count\': 96, \'index\': 106, \'type\': \'tables-info\'}, page_content=\'## Table Name: `titles`\\n\\n- **Description**: Tracks the job titles held by employees over time.\\n- **Composite Primary Key**: `emp_no`, `from_date`\\n- **Foreign Key**:\\n    - `emp_no`: References `employees(emp_no)`\\n\\n### Columns:\\n- `emp_no`: Employee number.\\n- `title`: Job title.\\n- `from_date`: Start date of the title.\\n- `to_date`: End date of the title.\'), Document(id=\'07c39ce6-a58f-4363-8083-647f31de551c\', metadata={\'source\': \'d:\\\\code\\\\text2sql\\\\data\\\\tables\\\\salaries.md\', \'table_name\': \'salaries\', \'token_count\': 98, \'index\': 105, \'type\': \'tables-info\'}, page_content=\'## Table Name: `salaries`\\n\\n- **Description**: Details the salary history of each employee.\\n- **Composite Primary Key**: `emp_no`, `from_date`\\n- **Foreign Key**:\\n    - `emp_no`: References `employees(emp_no)`\\n\\n### Columns:\\n- `emp_no`: Employee number.\\n- `salary`: Salary amount.\\n- `from_date`: Start date of the salary period.\\n- `to_date`: End date of the salary period.\')]', name='combined_retriever', tool_call_id='call_j7WbAGi0MnVyVKcERuuVVEDG'),
#   AIMessage(content='{"sql_query": "SHOW TABLES;", "explanation": "The query uses the SHOW TABLES command to list all tables in the current database. The tables are \'departments\', \'employees\', \'titles\', and \'salaries\' as identified from the provided table information."}', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 59, 'prompt_tokens': 1179, 'total_tokens': 1238, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4.1-nano-2025-04-14', 'system_fingerprint': 'fp_93ba275753', 'id': 'chatcmpl-D4SJTA619vyGTANvDvzRMfQr0H3rP', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019c1982-a895-7a01-9c39-fcbedf6381a4-0', usage_metadata={'input_tokens': 1179, 'output_tokens': 59, 'total_tokens': 1238, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})],
#  'tool_called': True}

        st.session_state.retrieved_docs = tool_messages_to_documents_json(response['messages']) 
        st.session_state.response = json.loads(response['messages'][-1].to_json()['kwargs']['content'])
    
    # Display explanation
    if st.session_state.response:
        st.write(st.session_state.response.get('explanation', 'No explanation provided'))
        
        # Display SQL query if not null
        sql_query = st.session_state.response.get('sql_query')
        if sql_query:
            st.subheader("SQL Query")
            st.code(sql_query, language="sql", wrap_lines=True)

                # Display retrieved documents (if available)
            if 'retrieved_docs' in st.session_state and st.session_state.retrieved_docs:
                with st.expander("📚 Retrieved Context", expanded=False):
                    # Separate documents by type
                    sample_queries = [doc for doc in st.session_state.retrieved_docs if doc.get('metadata', {}).get('type') == 'sample-queries']
                    table_info = [doc for doc in st.session_state.retrieved_docs if doc.get('metadata', {}).get('type') == 'tables-info']
                    
                    # Create tabs if we have both types
                    if sample_queries and table_info:
                        tab1, tab2 = st.tabs([f"📝 Sample Queries ({len(sample_queries)})", f"📊 Table Info ({len(table_info)})"])
                        
                        with tab1:
                            for idx, doc in enumerate(sample_queries, 1):
                                with st.container():
                                    st.markdown(f"**{idx}. {doc['page_content']}**")
                                    if 'sql' in doc.get('metadata', {}):
                                        st.code(doc['metadata']['sql'], language="sql")
                                    st.divider()
                        
                        with tab2:
                            for idx, doc in enumerate(table_info, 1):
                                table_name = doc.get('metadata', {}).get('table_name', f'Document {idx}')
                                with st.expander(f"📋 {table_name}"):
                                    st.markdown(doc['page_content'].replace('\\n','\n'), unsafe_allow_html=True)
                    
                    # If only one type exists
                    elif sample_queries:
                        for idx, doc in enumerate(sample_queries, 1):
                            with st.container():
                                st.markdown(f"**{idx}. {doc['page_content']}**")
                                if 'sql' in doc.get('metadata', {}):
                                    st.code(doc['metadata']['sql'], language="sql")
                                st.divider()
                    
                    elif table_info:
                        for idx, doc in enumerate(table_info, 1):
                            table_name = doc.get('metadata', {}).get('table_name', f'Document {idx}')
                            with st.expander(f"📋 {table_name}"):
                                st.markdown(doc['page_content'])
            
            with st.spinner("Running query..."):
                # import pandas as pd
                # df = pd.DataFrame({
                #     'emp_no': [10001, 10002],
                #     'first_name': ['Alice', 'Betty'],
                #     'last_name': ['Baaz', 'Baaz']
                # })
     
                
                df = run_query_df(sql_query)
                st.session_state.df_result = df
            
            if st.session_state.df_result is not None and not st.session_state.df_result.empty:
                st.subheader("Results")
                st.dataframe(st.session_state.df_result, width='stretch')
            elif st.session_state.df_result is not None:
                st.info("Query executed successfully but returned no results.")