from config import OPENAI_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
from telegram_bot import envoyer_message
import asyncio
import os
import schedule
import time

API_KEY = os.getenv("TWELVE_DATA_API_KEY")

# Analyse toutes les 5 min pour les opportunités
async def analyser_opportunites():
    print(f"[{time.strftime('%H:%M:%S')}] 🔄 Analyse des opportunités lancée")
    symboles = SYMBOLS.split(",")
    for symbole in symboles:
        try:
            heure, indicateurs = recuperer_donnees(symbole.strip(), API_KEY)
            analyse = generer_signal_ia(symbole, heure, indicateurs)

            # Vérifie que GPT retourne un taux de réussite ≥ 60%
            if analyse and "taux de réussite" in analyse.lower() and "%" in analyse:
                import re
                taux = re.search(r"(\d{1,3})\s*%", analyse)
                if taux and int(taux.group(1)) >= 60:
                    await envoyer_message(f"💡 Opportunité détectée sur {symbole} ({heure})\n{analyse}")
        except Exception as e:
            print(f"❌ Erreur sur {symbole} : {e}")

# Analyse globale toutes les heures
async def analyser_globale():
    symboles = SYMBOLS.split(",")
    resume_global = f"📊 Analyse globale {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    for symbole in symboles:
        try:
            heure, indicateurs = recuperer_donnees(symbole.strip(), API_KEY)
            analyse = generer_signal_ia(symbole, heure, indicateurs)
            resume_global += f"✅ {symbole}\n"
        except Exception as e:
            resume_global += f"❌ {symbole} : {e}\n"
    await envoyer_message(resume_global)

# Planification
def run_async(func):
    asyncio.run(func())

schedule.every(5).minutes.do(run_async, analyser_opportunites)
schedule.every().hour.at(":00").do(run_async, analyser_globale)

if __name__ == "__main__":
    print("✅ Bot lancé. Attente des prochaines exécutions...")
    run_async(analyser_opportunites)  # 🔁 Lancement immédiat
    while True:
        schedule.run_pending()
        time.sleep(1)
