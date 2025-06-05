import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("TWELVE_API_KEY")

if not all([TOKEN, CHAT_ID, API_KEY]):
    raise ValueError("❌ Variable d'environnement manquante.")
