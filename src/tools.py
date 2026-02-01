
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config.settings import TESTING, EMBEDDING_MODEL, VECTOR_DB_DIR_TABLES, VECTOR_DB_DIR_SAMPLEQ, VECTOR_DB_COMBINE


def table_info_retriever(user_query: str) -> list[str]:
    """
    Retrieve relevant table schema and information based on the user query.
    Returns a list of document contents.
    """
    if TESTING:
        return ["Dummy context"]
    
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    faiss_db = FAISS.load_local(VECTOR_DB_DIR_TABLES, embeddings, allow_dangerous_deserialization=True)
    results = faiss_db.similarity_search(user_query, k=3)

    return [doc.page_content for doc in results]

def sample_query_retriever(user_query: str) -> list[str]:
    """
    Retrieve relevant sample queries based on the user query.
    Returns a list of document contents.
    """
    if TESTING:
        return ["Dummy context"]
    
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    faiss_db = FAISS.load_local(VECTOR_DB_DIR_SAMPLEQ, embeddings, allow_dangerous_deserialization=True)
    results = faiss_db.similarity_search(user_query, k=3)

    return [doc.page_content for doc in results]

@tool
def combined_retriever(user_query:str):
    """
    Retrieve relevant table schema and sample queries based on the user query.
    """
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    faiss_db = FAISS.load_local(VECTOR_DB_COMBINE, embeddings, allow_dangerous_deserialization=True)
    results = faiss_db.similarity_search(user_query, k=5)

    # return [{'source':doc.metadata.get('source'), 'type':doc.metadata.get('type'), 'content':doc.page_content, 'sql'} for doc in results]
    return results


def reranker_retriever(user_query: str) -> str:
    """
    Retrieve relevant table schema and sample queries based on the user query.
    Then rerank them to provide the most relevant context for SQL generation.
    """
    # if TESTING:
    #     return "Dummy context"

    table_docs = table_info_retriever(user_query)
    sample_docs = sample_query_retriever(user_query)
    
    all_docs = table_docs + sample_docs
    
    if not all_docs:
        return ""

    from sentence_transformers import CrossEncoder
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    pairs = [[user_query, doc] for doc in all_docs]
    scores = model.predict(pairs)
    
    # Sort by score descending
    scored_docs = sorted(zip(scores, all_docs), key=lambda x: x[0], reverse=True)
    
    # Take top 3
    top_docs = [doc for score, doc in scored_docs[:3]]
    
    context = ""
    for doc in top_docs:
        context += doc
        context += "\n" + "=" * 10 + "\n"
        
    return context


def get_tool_messages(messages: list, tool_name: str | None = None) -> list:
    """
    Extracts the `content` from messages whose role is 'tool'.

    Args:
        messages: Iterable of message objects or dicts. Each message can be a dict
            with keys like 'role', 'name', and 'content', or an object with those
            attributes.
        tool_name: If provided, only return messages coming from a tool with this name.

    Returns:
        A list of message `content` values for matching tool messages.
    """
    results = []
    for m in messages:
        # get role
        role = None
        if isinstance(m, dict):
            role = m.get('role')
        else:
            role = getattr(m, 'role', None)

        if role != 'tool':
            continue

        # extract name and content
        name = None
        content = None
        if isinstance(m, dict):
            name = m.get('name') or m.get('tool')
            content = m.get('content')
            # sometimes content itself is a dict with a name field
            if content and isinstance(content, dict) and not name:
                name = content.get('name')
        else:
            name = getattr(m, 'name', None)
            content = getattr(m, 'content', None)

        if tool_name is None or name == tool_name:
            results.append(content)

    return results


def get_first_tool_message(messages: list, tool_name: str | None = None):
    """
    Return the first matching tool message content or None.
    """
    msgs = get_tool_messages(messages, tool_name=tool_name)
    return msgs[0] if msgs else None