import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

if not all([TOKEN, CHAT_ID, OPENAI_API_KEY, TWELVE_DATA_API_KEY]):
    raise ValueError("❌ Variable d'environnement manquante.")

SYMBOLS = {
    "XAUUSD": {
        "symbol": "XAU/USD",
        "interval": "5min",
        "actif": "XAUUSD"
    },
    "BTCUSD": {
        "symbol": "BTC/USD",
        "interval": "5min",
        "actif": "BTCUSD"
    },
    "NASDAQ": {
        "symbol": "QQQ",
        "interval": "5min",
        "actif": "NASDAQ"
    }
}
