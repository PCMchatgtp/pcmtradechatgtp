import os

# 🔐 Token Telegram et chat ID
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ✅ Liste des actifs à analyser
SYMBOLS = {
    "APPLE": "AAPL"
}


# ✅ Clé API OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# ✅ Paramètres de seuils
MIN_RR_TP1 = 1.0  # Ratio gain/risque minimal sur TP1
