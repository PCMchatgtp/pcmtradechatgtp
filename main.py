from config import OPENAI_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
import asyncio
from telegram_bot import envoyer_message
import os

print("✅ Imports réussis et clé OpenAI chargée :", bool(OPENAI_API_KEY))

API_KEY = os.getenv("TWELVE_DATA_API_KEY")

async def analyser_actifs():
    symboles = SYMBOLS.split(",")
    resume_global = "📊 Analyse globale\n"
    for symbole in symboles:
        try:
            heure, indicateurs = recuperer_donnees(symbole.strip(), API_KEY)
            analyse = generer_signal_ia(symbole, heure, indicateurs)
            await envoyer_message(f"💡 {symbole} ({heure})\n{analyse}")
            resume_global += f"✅ {symbole}\n"
        except Exception as e:
            resume_global += f"❌ {symbole} : {e}\n"
    await envoyer_message(resume_global)

import time

if __name__ == "__main__":
    while True:
        asyncio.run(analyser_actifs())
        time.sleep(3600)  # Pause d'une heure (3600 secondes) entre chaque analyse globale
