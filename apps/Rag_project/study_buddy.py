from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings



model = genai.GenerativeModel("gemini-2.5-flash-lite")
response = model.generate_content("Explain transformers in simple terms for a student")
print(response.text)

loader = PyPDFLoader("../data/windows_system_detailed_report.pdf")
documents = loader.load()

# print(len(documents))
# print(documents[0].page_content)
### Chunking

text_spllitters = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap=100
)
chunk = text_spllitters.split_documents(documents)
print("Total chunks:", len(chunk))

print(chunk[0].page_content)
print("------------------------------------")
print(chunk[1].page_content)
### Create Vector Database

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
vector_db = Chroma.from_documents(
    documents=chunk,
    embedding=embeddings,
    persist_directory="vectore_db"
)

print("vectore DB creadted!")
print(embeddings)
query = input("Ask your study buddy: ")
results = vector_db.similarity_search(query, k=3)
context = "\n\n".join([doc.page_content for doc in results])

# Build prompt
prompt = f"""
You are a helpful study assistant.

Use the following context to answer the question.

Context:
{context}

Question:
{query}

Answer clearly for a student. 
""" 
# Generate answer
response = model.generate_content(prompt)

print("\n📚 Study Buddy Answer:\n")
print(response.text)

if __name__ == "__main__":
    study_buddy.run(host="[IP_ADDRESS]", port=5000)
