# file: text2sql_chain.py
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from config.settings import EMBEDDING_MODEL, MODEL, VECTOR_DB_DIR_TABLES, TESTING
from config.logging_config import get_logger
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from src.tools import table_info_retriever

logger = get_logger('src/llm')

class SQLResponse(BaseModel):
    sql_query: str = Field(..., description="The MySQL query that answers the user request.")
    explanation: str = Field(..., description="A short explanation mentioning which tables were used in the query.")


parser = PydanticOutputParser(pydantic_object=SQLResponse)

text2sql_prompt = PromptTemplate(
    input_variables=["table_info", "user_query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    template="""
You are an expert MySQL developer. Your task is to generate a correct and optimized MySQL query based on:
1. The relevant table schema and details.
2. The user's natural language request.

Table Information:
{table_info}

User Question:
{user_query}

Instructions:
- Use only the tables and columns provided in the Table Information section.
- Do not make up any columns or tables.
- Ensure the query is syntactically valid for MySQL.
- Follow the output format provided below.

Output Format:
{format_instructions}
"""
)

llm = ChatOpenAI(model=MODEL)

def llm_with_metadata(prompt: str):
    """Wrapper to call LLM and return both parsed output + metadata."""
    if TESTING:
        logger.info('-----TESTING MODE-----DUMMY LLM OUTPUT')
        return return_llm_output()
    
    raw_response = llm.invoke(prompt)
    metadata = raw_response.response_metadata if hasattr(raw_response, "response_metadata") else {}
    parsed = parser.invoke(raw_response)
    return {
        "sql_query": parsed.sql_query,
        "explanation": parsed.explanation,
        "metadata": metadata
    }

text2sql_chain = (
    {
        "table_info": RunnableLambda(lambda x: table_info_retriever(x)),
        "user_query": RunnablePassthrough()
    }
    | text2sql_prompt
    | RunnableLambda(lambda prompt: llm_with_metadata(prompt))
)



def main():
    query = "total employees by job titles"
    result = text2sql_chain.invoke(query)

    print("SQL Query:\n", result["sql_query"])
    print("\nExplanation:\n", result["explanation"])
    print("\nMetadata:")
    for k, v in result["metadata"].items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
