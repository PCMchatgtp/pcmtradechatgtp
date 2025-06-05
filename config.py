import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

SYMBOLS = {
    "XAUUSD": os.getenv("SYMBOL_XAUUSD", "XAU/USD"),
    "BTCUSD": os.getenv("SYMBOL_BTCUSD", "BTC/USD"),
    "NASDAQ": os.getenv("SYMBOL_NASDAQ", "NDX")
}

if not all([TOKEN, CHAT_ID, TWELVE_DATA_API_KEY]):
    raise ValueError("❌ Variable d'environnement manquante.")
