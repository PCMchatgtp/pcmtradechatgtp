import os

# Clés à mettre dans les variables Render (pas en dur ici)
TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
SYMBOLS = {
    "XAUUSD": "XAUUSD=X",
    "NASDAQ": "^IXIC",
    "DAX": "^GDAXI"
}
