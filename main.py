from config import OPENAI_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
from telegram_bot import envoyer_message
import os
from datetime import datetime
import pytz

api_key = os.getenv("TWELVE_DATA_API_KEY")
paris = pytz.timezone("Europe/Paris")
maintenant = datetime.now(paris).strftime("%Y-%m-%d %H:%M:%S")

resume = f"📊 Analyse globale {maintenant}\n"

for symbole in SYMBOLS:
    try:
        tendance, heure, indicateurs = recuperer_donnees(symbole, api_key)
        message = generer_signal_ia(symbole, tendance, heure, indicateurs)
        envoyer_message(f"💡 {symbole}\n{message}")
        resume += f"✅ {symbole}\n"
    except Exception as e:
        resume += f"❌ {symbole} : {e}\n"

envoyer_message(resume.strip())