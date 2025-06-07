import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYMBOLS = ["BTC/USD", "XAU/USD", "QQQ"]

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID or not TWELVE_DATA_API_KEY or not OPENAI_API_KEY:
    raise ValueError("❌ Variable d'environnement manquante.")