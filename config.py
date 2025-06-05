import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SYMBOLS = {
    "XAUUSD": "XAU/USD",
    "BTCUSD": "BTC/USD"
}
