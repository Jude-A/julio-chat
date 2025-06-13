# amourbot/main.py
import streamlit as st
from logic.responder import generate_response
from logic.memory import init_vectorstore
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Julio❤️",
    page_icon="",
    layout="centered"
)

# Vérification de la clé API
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ Clé API OpenAI manquante. Veuillez configurer votre clé API.")
    st.stop()

# Initialisation de la mémoire vectorielle
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = init_vectorstore()

# Initialisation de l'historique des messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Titre et description
st.title("Julio")
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar avec informations
with st.sidebar:
    st.title("💬 À propos")
    st.markdown("""
    Ce chat est une expérience personnelle.
    Merci de respecter la confidentialité des conversations.
    """)
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
user_input = st.chat_input("Dis moi?")

# Traitement de la réponse
if user_input:
    # Ajout du message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Génération de la réponse avec l'historique
    try:
        response = generate_response(
            user_input,
            st.session_state.vectorstore,
            st.session_state.messages[:-1]
        )
        
        # Ajout de la réponse de l'IA
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": "Désolé, j'ai rencontré une erreur. Pouvez-vous réessayer ?"})
    
    # Rafraîchissement de l'affichage
    st.rerun()