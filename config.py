import os

TOKEN = os.getenv("TOKEN")
ALPHAV_API_KEY = os.getenv("ALPHAV_API_KEY")
TWELVE_API_KEY = os.getenv("TWELVE_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")  # ✅ Pour les prix marché
FMP_API_KEY = os.getenv("FMP_API_KEY")          # ✅ Pour le calendrier économique
GOOGLE_SHEET_WEBHOOK = os.getenv("GOOGLE_SHEET_WEBHOOK")

print("TOKEN =", TOKEN)
print("CHAT_ID =", CHAT_ID)

if not TOKEN or not CHAT_ID:
    raise ValueError("❌ TOKEN ou CHAT_ID manquant dans Render.")
