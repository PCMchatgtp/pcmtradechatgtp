import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SYMBOLS = os.getenv("SYMBOLS")

if not all([OPENAI_API_KEY, TOKEN, CHAT_ID, SYMBOLS]):
    raise ValueError("❌ Une ou plusieurs variables d'environnement sont manquantes.")