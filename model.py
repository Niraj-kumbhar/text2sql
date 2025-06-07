from dotenv import load_dotenv
import os

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


load_dotenv()

loader = DirectoryLoader('./data/input/',glob='*_tbl.md')
documents = loader.load()

# get open ai embeddings
embedding = OpenAIEmbeddings(model='text-embedding-ada-002')

# store embeddings using chroma - './chroma/'
vector_store = Chroma(collection_name='mysql_employees_tables', embedding_function=embedding, persist_directory='./chroma/')

temp = vector_store.add_documents(documents=documents)

