from openai import OpenAI
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import streamlit as st

# Initialisation du client OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ Clé API OpenAI manquante. Veuillez configurer votre clé API dans les secrets de Streamlit Cloud.")
    st.stop()

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"⚠️ Erreur lors de l'initialisation du client OpenAI : {str(e)}")
    st.stop()

def get_embedding(text):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        st.error(f"⚠️ Erreur lors de la génération des embeddings : {str(e)}")
        return None

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
    embeddings = []
    for text in texts:
        embedding = get_embedding(text)
        if embedding:
            embeddings.append(embedding)
    
    if not embeddings:
        st.error("⚠️ Aucun embedding n'a pu être généré. Vérifiez votre clé API et vos textes.")
        st.stop()
    
    return {
        'texts': texts,
        'embeddings': np.array(embeddings)
    }

def search_memory(vectorstore, query, k=3):
    if not vectorstore['texts']:
        return []
        
    # Génère l'embedding de la requête
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return []
    
    # Calcule les similarités
    similarities = cosine_similarity([query_embedding], vectorstore['embeddings'])[0]
    
    # Trouve les k textes les plus similaires
    top_k_idx = np.argsort(similarities)[-k:][::-1]
    
    # Retourne les documents correspondants
    from langchain.docstore.document import Document
    return [Document(page_content=vectorstore['texts'][idx]) for idx in top_k_idx]
