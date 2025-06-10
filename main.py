from config import OPENAI_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
from telegram_bot import envoyer_message
import asyncio
import os
import schedule
import time
import re
from datetime import datetime, timedelta
import pytz

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
opr_fenetre_active = False
opr_debut = None

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
                    await asyncio.wait_for(
                        envoyer_message(f"💡 Opportunité détectée sur {symbole} ({heure})\n{analyse}"), timeout=10
                    )

        except asyncio.TimeoutError:
            print(f"⏱️ Timeout sur {symbole} – Telegram trop lent", flush=True)
        except Exception as e:
            print(f"❌ Erreur sur {symbole} : {e}", flush=True)

# Analyse OPR spécifique Gold/BTC après 15h45 jusqu’à 16h15
async def analyser_opr():
    global opr_fenetre_active, opr_debut
    paris_tz = pytz.timezone("Europe/Paris")
    now = datetime.now(paris_tz)

    if not opr_fenetre_active:
        opr_fenetre_active = True
        opr_debut = now
        print(f"[{now.strftime('%H:%M:%S')}] 🚀 Fenêtre OPR démarrée")

    elif (now - opr_debut) > timedelta(minutes=30):
        opr_fenetre_active = False
        print(f"[{now.strftime('%H:%M:%S')}] ❌ Fin de la fenêtre OPR")
        return

    for symbole in ["XAU/USD", "BTC/USD"]:
        try:
            heure, indicateurs = recuperer_donnees(symbole, API_KEY)
            analyse = generer_signal_ia(symbole, heure, indicateurs)

            if analyse and "taux de réussite" in analyse.lower() and "%" in analyse:
                taux = re.search(r"(\d{1,3})\s*%", analyse)
                if taux and int(taux.group(1)) >= 60:
                    await envoyer_message(f"📈 Signal OPR détecté sur {symbole} ({heure})\n{analyse}")
                    opr_fenetre_active = False  # On stoppe après le premier trade détecté
        except Exception as e:
            print(f"❌ Erreur OPR sur {symbole} : {e}", flush=True)

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

# Wrapper sécurisé
def run_async(coroutine_func):
    loop = asyncio.get_event_loop()
    coroutine = coroutine_func()
    async def safe_wrapper():
        try:
            await coroutine
        except Exception as e:
            print(f"❌ Erreur dans {coroutine_func.__name__} : {e}", flush=True)

    if loop.is_running():
        asyncio.ensure_future(safe_wrapper())
    else:
        loop.run_until_complete(safe_wrapper())

# Boucle continue
async def boucle_schedule():
    while True:
        schedule.run_pending()
        print(f"🕒 {time.strftime('%H:%M:%S')} - En attente de la prochaine exécution...", flush=True)
        await asyncio.sleep(1)

# Lancement principal
async def main():
    print("✅ Bot lancé. Démarrage des premières analyses...", flush=True)
    run_async(analyser_opportunites)
    schedule.every(5).minutes.do(lambda: run_async(analyser_opportunites))
    schedule.every().hour.at(":00").do(lambda: run_async(analyser_globale))
    schedule.every().day.at("15:45").do(lambda: run_async(analyser_opr))
    schedule.every(5).minutes.do(lambda: run_async(analyser_opr))
    await boucle_schedule()

if __name__ == "__main__":
    asyncio.run(main())
