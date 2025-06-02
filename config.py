import os

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_ID = int(os.getenv("CHAT_ID"))

if not TOKEN or not CHAT_ID:
    raise ValueError("❌ TOKEN ou CHAT_ID manquant dans Render.")
