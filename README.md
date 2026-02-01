# 🤖 Text2SQL App

A powerful Streamlit-based AI Agent that allows users to explore and query SQL databases using natural language. Built with LangChain, LangGraph, and OpenAI.

![Architecture](./img/demo.gif)

## ✨ Features

- **Natural Language to SQL**: Convert English questions into valid MySQL queries.
- **RAG-Enhanced**: Uses Retrieval-Augmented Generation to understand table schemas and leverage sample queries for higher accuracy.
- **Interactive UI**: User-friendly chat interface built with Streamlit.
- **Data Visualization**: Automatically executes queries and displays results in interactive tables.
- **Transparent Logic**: View the generated SQL and retrieved context (similar queries, table info) for verification.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+**
- **Poetry** (Dependency Manager)
- **MySQL Database**: You need the standard `employees` sample database installed and running locally.
- **OpenAI API Key**: Access to GPT-4 models.

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd text2sql
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

## ⚙️ Configuration

1. **Environment Variables**
   Create a `.env` file in the root directory with the following credentials:
   ```ini
   DB_USER=your_mysql_username
   DB_CRED=your_mysql_password
   OPENAI_API_KEY=your_openai_api_key
   ```

2. **Database Setup**
   Ensure your local MySQL instance has the `employees` database loaded. The agent is specifically tuned for this schema.

## 🖥️ Usage

1. **Start the Application**
   ```bash
   poetry run streamlit run text2sql.py
   ```

2. **Interact with the Agent**
   - Open your browser at `http://localhost:8501`.
   - Select the database from the sidebar (currently supports `employees`).
   - Type your question in the chat box (e.g., "Show me the count of employees by gender").
   - View the generated SQL, reasoning, and data results.

## 📂 Project Structure

- `src/`: Core application logic (agents, tools, SQL execution).
- `config/`: Configuration files and settings.
- `data/`: Table schemas and sample queries used for RAG.
- `text2sql.py`: Main entry point for the Streamlit app.