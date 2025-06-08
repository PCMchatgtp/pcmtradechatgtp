import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SYMBOLS = os.getenv("SYMBOLS", "XAU/USD,BTC/USD,QQQ")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

if not all([OPENAI_API_KEY, TOKEN, CHAT_ID, SYMBOLS, TWELVE_DATA_API_KEY]):
    raise ValueError("❌ Une ou plusieurs variables d'environnement sont manquantes.")
