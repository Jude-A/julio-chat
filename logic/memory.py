from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

# Initialisation du modèle d'embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def init_vectorstore():
    # Charge le fichier de souvenirs
    paths = ["data/souvenirs.txt"]
    raw_texts = []

    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                raw_texts += f.read().split("•")

    # Nettoie les textes
    texts = [txt.strip() for txt in raw_texts if txt.strip()]
    
    # Génère les embeddings
    embeddings = model.encode(texts)
    
    return {
        'texts': texts,
        'embeddings': embeddings
    }

def search_memory(vectorstore, query, k=3):
    # Génère l'embedding de la requête
    query_embedding = model.encode([query])[0]
    
    # Calcule les similarités
    similarities = cosine_similarity([query_embedding], vectorstore['embeddings'])[0]
    
    # Trouve les k textes les plus similaires
    top_k_idx = np.argsort(similarities)[-k:][::-1]
    
    # Retourne les documents correspondants
    from langchain.docstore.document import Document
    return [Document(page_content=vectorstore['texts'][idx]) for idx in top_k_idx]
