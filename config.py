import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

SYMBOLS = ["XAU/USD", "BTC/USD", "QQQ"]

if not OPENAI_API_KEY or not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID or not TWELVE_DATA_API_KEY:
    raise ValueError("❌ Une ou plusieurs variables d'environnement sont manquantes.")