import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SYMBOLS = os.getenv("SYMBOLS", "XAU/USD,BTC/USD,QQQ").split(",")

if not all([OPENAI_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS]):
    raise ValueError("❌ Une ou plusieurs variables d'environnement sont manquantes.")