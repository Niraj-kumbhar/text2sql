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

#         response = {'messages': [HumanMessage(content='give me count of employees gender wise in each department', additional_kwargs={}, response_metadata={}),
#   AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 27, 'prompt_tokens': 351, 'total_tokens': 378, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4.1-nano-2025-04-14', 'system_fingerprint': 'fp_93ba275753', 'id': 'chatcmpl-D4TUbT5XTkcAmWLPwiesnspOEL7h4', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--019c19c7-d86e-7642-9254-4a30ac430f3d-0', tool_calls=[{'name': 'combined_retriever', 'args': {'user_query': 'give me count of employees gender wise in each department'}, 'id': 'call_c7g6GSBeGLzATSRtOlLni9yN', 'type': 'tool_call'}], usage_metadata={'input_tokens': 351, 'output_tokens': 27, 'total_tokens': 378, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}),
#   ToolMessage(content='[Document(id=\'08eeab66-1b46-4c75-a44c-c02d3c9444b6\', metadata={\'sql\': "SELECT d.dept_name, COUNT(de.emp_no) AS employee_count\\nFROM departments d\\nJOIN dept_emp de ON d.dept_no = de.dept_no\\nWHERE de.to_date = \'9999-01-01\'\\nGROUP BY d.dept_name\\nORDER BY employee_count DESC;", \'source\': \'queries.json\', \'index\': 2, \'type\': \'sample-queries\', \'token_count\': 8}, page_content=\'Find the number of employees per department.\'), Document(id=\'8f35b281-22d9-4fa3-b1b9-b29fca92094f\', metadata={\'sql\': "SELECT \\n    d.dept_name, \\n    e.first_name, \\n    e.last_name\\nFROM dept_manager dm\\nJOIN departments d ON dm.dept_no = d.dept_no\\nJOIN employees e ON dm.emp_no = e.emp_no\\nWHERE dm.to_date = \'9999-01-01\';", \'source\': \'queries.json\', \'index\': 3, \'type\': \'sample-queries\', \'token_count\': 10}, page_content=\'Get the list of department managers and their departments.\'), Document(id=\'e3b9593b-fbe6-47f3-bf53-83d72d9683f9\', metadata={\'sql\': "SELECT d.dept_name, AVG(s.salary) AS avg_salary\\nFROM departments d\\nJOIN dept_emp de ON d.dept_no = de.dept_no\\nJOIN salaries s ON de.emp_no = s.emp_no\\nWHERE de.to_date = \'9999-01-01\' AND s.to_date = \'9999-01-01\'\\nGROUP BY d.dept_name\\nORDER BY avg_salary DESC;", \'source\': \'queries.json\', \'index\': 5, \'type\': \'sample-queries\', \'token_count\': 7}, page_content=\'Get the average salary by department.\'), Document(id=\'566e7799-7006-4183-aa1e-463566881529\', metadata={\'source\': \'d:\\\\code\\\\text2sql\\\\data\\\\tables\\\\dep_manager.md\', \'table_name\': \'dep_manager\', \'token_count\': 117, \'index\': 103, \'type\': \'tables-info\'}, page_content=\'## Table Name: `dept_manager`\\n\\n- **Description**: Records the managerial assignments of employees to departments.\\n- **Composite Primary Key**: `dept_no`, `emp_no`, `from_date`\\n- **Foreign Keys**:\\n    - `dept_no`: References `departments(dept_no)`\\n    - `emp_no`: References `employees(emp_no)`\\n\\n### Columns:\\n- `dept_no`: Department number.\\n- `emp_no`: Employee number.\\n- `from_date`: Start date of the managerial assignment.\\n- `to_date`: End date of the managerial assignment.\'), Document(id=\'94cecafa-c14c-4bd3-ae67-614c96eb99b4\', metadata={\'source\': \'d:\\\\code\\\\text2sql\\\\data\\\\tables\\\\dep_emp.md\', \'table_name\': \'dep_emp\', \'token_count\': 122, \'index\': 102, \'type\': \'tables-info\'}, page_content=\'## Table Name: `dept_emp`\\n\\n- **Description**: Associates employees with the departments they have worked in, including the duration.\\n- **Composite Primary Key**: `emp_no`, `dept_no`, `from_date`\\n- **Foreign Keys**:\\n    - `emp_no`: References `employees(emp_no)`\\n    - `dept_no`: References `departments(dept_no)`\\n\\n### Columns:\\n- `emp_no`: Employee number.\\n- `dept_no`: Department number.\\n- `from_date`: Start date of the department assignment.\\n- `to_date`: End date of the department assignment.\')]', name='combined_retriever', tool_call_id='call_c7g6GSBeGLzATSRtOlLni9yN'),
#   AIMessage(content='{"sql_query": "SELECT d.dept_name, e.gender, COUNT(e.emp_no) AS employee_count\\nFROM departments d\\nJOIN dept_emp de ON d.dept_no = de.dept_no\\nJOIN employees e ON de.emp_no = e.emp_no\\nWHERE de.to_date = \'9999-01-01\'\\nGROUP BY d.dept_name, e.gender\\nORDER BY d.dept_name, e.gender;", "explanation": "The query uses the \'departments\', \'dept_emp\', and \'employees\' tables to count employees grouped by department and gender."}', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 120, 'prompt_tokens': 1200, 'total_tokens': 1320, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4.1-nano-2025-04-14', 'system_fingerprint': 'fp_93ba275753', 'id': 'chatcmpl-D4TUftPslC46c4QkISlaMfvevFk6N', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019c19c7-e456-7180-b5f0-8a483c32c8fa-0', usage_metadata={'input_tokens': 1200, 'output_tokens': 120, 'total_tokens': 1320, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})],
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