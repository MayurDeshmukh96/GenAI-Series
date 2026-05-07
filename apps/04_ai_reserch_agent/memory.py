from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)               

# Vector database for memoryss
memory_db = Chroma(
    persist_directory="agent_memory",
    embedding_function=embeddings
)

# Memory functions
def save_memory(text):
    """Save information to memory"""
    memory_db.add_texts([text])
    print(f"Memory saved: {text}")

def retrieve_memory(query, k=3):
    """Retrieve relevant information from memory"""
    results = memory_db.similarity_search(query, k=k)
    return [doc.page_content for doc in results]

