import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

SYMBOLS = ["XAUUSD", "NASDAQ", "DAX"]

if not TOKEN or not CHAT_ID:
    raise ValueError("❌ TOKEN ou CHAT_ID manquant dans Render.")
