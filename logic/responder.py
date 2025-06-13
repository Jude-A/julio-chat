# logic/responder.py
from openai import OpenAI
from logic.memory import search_memory
from logic.prompts import build_prompt
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    # Appel à l'API OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

print("Clé chargée :", (os.getenv("OPENAI_API_KEY") or "")[:8] + "...")
