from config import OPENAI_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
from telegram_bot import envoyer_message
import asyncio
import os
import schedule
import time
import re

API_KEY = os.getenv("TWELVE_DATA_API_KEY")

# Analyse toutes les 5 min pour les opportunités
async def analyser_opportunites():
    print(f"[{time.strftime('%H:%M:%S')}] 🔄 Analyse des opportunités lancée", flush=True)
    symboles = SYMBOLS.split(",")
    for symbole in symboles:
        try:
            heure, indicateurs = recuperer_donnees(symbole.strip(), API_KEY)
            analyse = generer_signal_ia(symbole, heure, indicateurs)

            if not analyse or "aucune opportunité" in analyse.lower():
                print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Aucune opportunité détectée sur {symbole}", flush=True)
                continue

            if "taux de réussite" in analyse.lower() and "%" in analyse:
                taux = re.search(r"(\d{1,3})\s*%", analyse)
                if taux and int(taux.group(1)) >= 60:
                    await envoyer_message(f"💡 Opportunité détectée sur {symbole} ({heure})\n{analyse}")
        except Exception as e:
            print(f"❌ Erreur sur {symbole} : {e}", flush=True)

# Analyse globale toutes les heures
async def analyser_globale():
    print(f"[{time.strftime('%H:%M:%S')}] 🧠 Analyse globale lancée", flush=True)
    symboles = SYMBOLS.split(",")
    resume_global = f"📊 Analyse globale {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    for symbole in symboles:
        try:
            heure, indicateurs = recuperer_donnees(symbole.strip(), API_KEY)
            generer_signal_ia(symbole, heure, indicateurs)
            resume_global += f"✅ {symbole}\n"
        except Exception as e:
            resume_global += f"❌ {symbole} : {e}\n"
    await envoyer_message(resume_global)

# Fonction pour exécuter une coroutine depuis une fonction synchrone
def run_async(coro):
    asyncio.run(coro())

# Lancement du bot
if __name__ == "__main__":
    print("✅ Bot lancé. Démarrage des premières analyses...", flush=True)

    # Lancement initial
    run_async(analyser_opportunites)

    # Planification
    schedule.every(5).minutes.do(lambda: run_async(analyser_opportunites))
    schedule.every().hour.at(":00").do(lambda: run_async(analyser_globale))

    # Boucle principale
    while True:
        schedule.run_pending()
        print(f"🕒 {time.strftime('%H:%M:%S')} - En attente de la prochaine exécution...", flush=True)
        time.sleep(60)
