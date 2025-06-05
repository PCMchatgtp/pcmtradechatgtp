import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

SYMBOLS = {
    "XAUUSD": {"symbol": "XAU/USD", "heure_debut": 7, "heure_fin": 22},
    "BTCUSD": {"symbol": "BTC/USD", "heure_debut": 7, "heure_fin": 22},
    "NASDAQ": {"symbol": "NDX", "heure_debut": 15, "heure_fin": 18},
}
