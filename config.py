import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

SYMBOLS = {
    "XAUUSD": {"symbol": "XAU/USD", "start_hour": 7, "end_hour": 22},
    "NASDAQ": {"symbol": "QQQ", "start_hour": 15, "end_hour": 18},
    "BTCUSD": {"symbol": "BTC/USD", "start_hour": 7, "end_hour": 22},
}
