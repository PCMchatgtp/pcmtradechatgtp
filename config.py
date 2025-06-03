import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

if not TOKEN or not CHAT_ID or not TWELVE_DATA_API_KEY:
    raise ValueError("❌ Variable d'environnement manquante.")

SYMBOLS = {
    "XAUUSD": "XAU/USD",
    "NASDAQ": "QQQ"
}
