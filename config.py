import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYMBOLS = {
    "XAU/USD": "XAU/USD",
    "BTC/USD": "BTC/USD",
    "NASDAQ": "QQQ"
}
