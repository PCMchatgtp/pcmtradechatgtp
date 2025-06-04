import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")

if not TOKEN or not CHAT_ID or not TWELVEDATA_API_KEY:
    raise ValueError("❌ Variable d'environnement manquante.")

SYMBOLS = {
    "XAUUSD": "XAU/USD",
    "NASDAQ": "NDX"
}
