import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
twelve_data_api_key = os.getenv("TWELVE_DATA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYMBOLS = ["XAU/USD", "BTC/USD", "QQQ"]

if not all([TOKEN, CHAT_ID, twelve_data_api_key, OPENAI_API_KEY]):
    raise ValueError("❌ Variable d'environnement manquante.")