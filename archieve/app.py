import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.agents import agent_app
from langchain_core.messages import BaseMessage, HumanMessage

# Page config
st.set_page_config(
    page_title="Text2SQL Agent",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        color: #1f1f1f;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .user-message {
        background-color: #e8e8e8;
        margin-left: 15%;
    }
    .assistant-message {
        background-color: #d4e8f0;
        margin-right: 15%;
    }
    
    /* Header styling */
    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    .title-section {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .title-section h1 {
        color: #fafafa;
        font-size: 2rem;
        margin: 0;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton button {
        background-color: transparent;
        border: 1px solid #4a4a4a;
        color: #fafafa;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton button:hover {
        border-color: #6a6a6a;
        background-color: #1a1a1a;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        background-color: #1a1a1a;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
    
    /* Toggle and select boxes */
    .stToggle label {
        color: #fafafa !important;
    }
    .stSelectbox label {
        color: #fafafa !important;
        font-weight: 500;
    }
    
    /* Chat input area */
    .stChatInput {
        border-top: 1px solid #2a2a2a;
        padding-top: 1rem;
        margin-top: 2rem;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #6a6a6a;
        font-size: 0.85rem;
        padding: 1rem 0 0.5rem 0;
        border-top: 1px solid #2a2a2a;
        margin-top: 1rem;
    }
    
    /* Remove extra margins */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'show_chart' not in st.session_state:
    st.session_state.show_chart = {}

# Header
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown('<div class="title-section"><span style="font-size: 2rem;">💬</span><h1>Text2SQL Agent</h1></div>', unsafe_allow_html=True)
with col2:
    if st.button("🔄 New Chat", width='stretch'):
        st.session_state.messages = []
        st.session_state.show_chart = {}
        st.rerun()

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <b>You:</b><br>{message["content"]}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <b>Agent:</b><br>{message["content"]}
            </div>
        """, unsafe_allow_html=True)
        
        # Display dataframe if available
        if "dataframe" in message:
            df = message["dataframe"]
            st.dataframe(df, width='stretch')
            
            # Chart toggle and options
            chart_key = f"chart_{idx}"
            show_chart = st.toggle("📊 Show Chart", key=f"toggle_{idx}", 
                                  value=st.session_state.show_chart.get(chart_key, True))
            st.session_state.show_chart[chart_key] = show_chart
            
            if show_chart:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    chart_type = st.selectbox(
                        "Chart Type",
                        ["Bar", "Line", "Scatter", "Pie", "Area"],
                        key=f"chart_type_{idx}"
                    )
                
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                all_cols = df.columns.tolist()
                
                with col2:
                    if chart_type != "Pie":
                        x_axis = st.selectbox(
                            "X-Axis",
                            all_cols,
                            key=f"x_axis_{idx}"
                        )
                    else:
                        x_axis = st.selectbox(
                            "Labels",
                            all_cols,
                            key=f"labels_{idx}"
                        )
                
                with col3:
                    if chart_type != "Pie":
                        y_axis = st.selectbox(
                            "Y-Axis",
                            numeric_cols if numeric_cols else all_cols,
                            key=f"y_axis_{idx}"
                        )
                    else:
                        y_axis = st.selectbox(
                            "Values",
                            numeric_cols if numeric_cols else all_cols,
                            key=f"values_{idx}"
                        )
                
                # Generate chart
                try:
                    if chart_type == "Bar":
                        fig = px.bar(df, x=x_axis, y=y_axis)
                    elif chart_type == "Line":
                        fig = px.line(df, x=x_axis, y=y_axis)
                    elif chart_type == "Scatter":
                        fig = px.scatter(df, x=x_axis, y=y_axis)
                    elif chart_type == "Pie":
                        fig = px.pie(df, names=x_axis, values=y_axis)
                    elif chart_type == "Area":
                        fig = px.area(df, x=x_axis, y=y_axis)
                    
                    fig.update_layout(
                        height=400,
                        margin=dict(l=20, r=20, t=40, b=20),
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#fafafa')
                    )
                    st.plotly_chart(fig, width='stretch')
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")

# Chat input
user_input = st.chat_input("Ask a question about your data...")

# Footer - appears below chat input
st.markdown(
    '<div class="footer-text">Text2SQL Agent | Powered by AI</div>',
    unsafe_allow_html=True
)

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # PLACEHOLDER: Replace this with your actual agent call
    # Example agent response with dataframe
    with st.spinner("Agent is processing..."):
        # Simulated agent response
        agent_response = agent_app.invoke({"messages": [HumanMessage(content=user_input)]})

        st.session_state.messages.append({
            "role": "assistant",
            "content": agent_response,
        })
        
        # # Simulated dataframe (replace with actual agent output)
        # sample_df = pd.DataFrame({
        #     'Category': ['A', 'B', 'C', 'D', 'E'],
        #     'Sales': [100, 200, 150, 300, 250],
        #     'Profit': [20, 40, 30, 60, 50]
        # })
        
        # # Check if agent returns a dataframe
        # # Replace this condition with your actual logic
        # has_dataframe = True  # Set to True if agent returns dataframe
        
        # if has_dataframe:
        #     st.session_state.messages.append({
        #         "role": "assistant",
        #         "content": agent_response,
        #         "dataframe": sample_df
        #     })
        # else:
        #     st.session_state.messages.append({
        #         "role": "assistant",
        #         "content": agent_response
        #     })
    
    st.rerun()