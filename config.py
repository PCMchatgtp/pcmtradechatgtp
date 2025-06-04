import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("❌ Variable d'environnement manquante.")

SYMBOLS = {
    "XAUUSD": {"twelve_symbol": "XAU/USD", "timezone": "Etc/UTC"},
    "NASDAQ": {"twelve_symbol": "qqq", "timezone": "America/New_York"}
}
