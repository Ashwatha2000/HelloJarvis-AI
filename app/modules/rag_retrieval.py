import os
from langchain_community.vectorstores import FAISS  # ✅ Updated Import
from langchain_community.embeddings import HuggingFaceEmbeddings  # ✅ Updated Import
from langchain_community.document_loaders import TextLoader  # ✅ Updated Import
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ✅ Load the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def index_knowledge_base():
    """Reads knowledge_base/ and stores data in FAISS for retrieval."""
    documents = []
    knowledge_path = "knowledge_base"  # 📂 The only folder it processes

    # ✅ Loop through all .txt files in knowledge_base/
    for file in os.listdir(knowledge_path):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(knowledge_path, file))
            documents.extend(loader.load())

    # ✅ Split text into smaller chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # ✅ Store processed data in FAISS
    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local("faiss_index")  # 📂 Saves FAISS data separately
    print("✅ Knowledge base indexed successfully! 🚀")

def retrieve_knowledge(user_query):
    """Retrieves relevant knowledge from FAISS based on a query."""
    vectorstore = FAISS.load_local("faiss_index", embedding_model)  # Load FAISS storage
    retrieved_docs = vectorstore.similarity_search(user_query, k=3)  # Retrieve top 3 matches
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    return context  # Returns the most relevant data
