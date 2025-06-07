import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
twelve_data_api_key = os.getenv("TWELVE_DATA_API_KEY")

SYMBOLS = ["BTC/USD", "XAU/USD", "QQQ"]

if not all([TOKEN, CHAT_ID, OPENAI_API_KEY, twelve_data_api_key]):
    raise ValueError("❌ Variable d'environnement manquante.")