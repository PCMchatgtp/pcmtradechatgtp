import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TWELVE_DATA_API_KEY = os.getenv("twelve_data_api_key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")
SYMBOLS = {
    "XAUUSD": {"symbol": "XAU/USD", "heure_debut": 7, "heure_fin": 22},
    "BTCUSD": {"symbol": "BTC/USD", "heure_debut": 7, "heure_fin": 22},
    "NASDAQ": {"symbol": "NDX", "heure_debut": 15, "heure_fin": 18},
}


if not all([TOKEN, CHAT_ID, TWELVE_DATA_API_KEY]):
    raise ValueError("❌ Variable d'environnement manquante.")
