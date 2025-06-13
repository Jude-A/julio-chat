from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
import os

def init_vectorstore():
    # Charge le fichier de souvenirs
    paths = ["data/souvenirs.txt"]
    raw_texts = []

    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                raw_texts += f.read().split("•")

    # Nettoie et transforme en documents
    documents = [Document(page_content=txt.strip()) for txt in raw_texts if txt.strip()]
    
    # Génère les embeddings et crée la base vectorielle
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    return vectorstore

def search_memory(vectorstore, query, k=3):
    return vectorstore.similarity_search(query, k=k)
