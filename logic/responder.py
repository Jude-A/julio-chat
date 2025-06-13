# logic/responder.py
from openai import OpenAI
from logic.memory import search_memory
from logic.prompts import build_prompt
import os
from dotenv import load_dotenv
import streamlit as st

# Chargement des variables d'environnement
load_dotenv()

# Récupération de la clé API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ Clé API OpenAI manquante. Veuillez configurer votre clé API dans les secrets de Streamlit Cloud.")
    st.stop()

# Initialisation du client OpenAI
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"⚠️ Erreur lors de l'initialisation du client OpenAI : {str(e)}")
    st.stop()

def generate_response(user_input, vectorstore, conversation_history=None):
    # Commande spéciale pour déclencher une surprise personnalisée
    if "!surprise" in user_input.lower():
        return "🎁 Tu as trouvé un message caché ! Va voir dans ton dossier 'surprises'... 😘"

    # Recherche de souvenirs pertinents
    memory_hits = search_memory(vectorstore, user_input)
    memory_context = "\n".join([doc.page_content for doc in memory_hits])

    # Construction du prompt avec humeur et souvenirs
    prompt = build_prompt(user_input, memory_context, conversation_history)

    # Préparation des messages pour l'API
    messages = [{"role": "system", "content": prompt}]
    
    # Ajout de l'historique de la conversation
    if conversation_history:
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Ajout du message actuel
    messages.append({"role": "user", "content": user_input})

    try:
        # Appel à l'API OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"⚠️ Erreur lors de l'appel à l'API OpenAI : {str(e)}")
        return "Désolé, j'ai rencontré une erreur. Pouvez-vous réessayer ?"

print("Clé chargée :", (os.getenv("OPENAI_API_KEY") or "")[:8] + "...")
