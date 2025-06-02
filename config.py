import os

# Récupération des variables d'environnement depuis Render
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Vérification (optionnel, utile pour debug)
if TOKEN is None or CHAT_ID is None:
    raise ValueError("❌ Les variables TOKEN ou CHAT_ID ne sont pas définies dans Render.")
