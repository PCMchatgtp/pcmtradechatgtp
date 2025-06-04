import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TWELVE_API_KEY = os.getenv("TWELVE_API_KEY")

SYMBOLS = {
   "XAUUSD": (7, 22),     # Gold : 7h à 22h
    "BTCUSD": (7, 22),     # BTC/USD : 7h à 22h
    "NASDAQ": (15.5, 18)   # NASDAQ : 15h30 à 18h
}
