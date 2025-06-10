from config import OPENAI_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia, generer_signal_opr
from telegram_bot import envoyer_message
import asyncio
import os
import schedule
import time
import re
from datetime import datetime
import pytz

API_KEY = os.getenv("TWELVE_DATA_API_KEY")

# Définition du range OPR à 15h45
opr_range = {}

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

# OPR (après 15h45 jusqu'à 16h15)
async def analyser_opr():
    paris_tz = pytz.timezone("Europe/Paris")
    now = datetime.now(paris_tz)
    heure_now = now.strftime("%H:%M")
    heure_int = int(now.strftime("%H%M"))
    if 1545 <= heure_int <= 1615:
        for symbole in ["BTC/USD", "XAU/USD"]:
            if symbole in opr_range:
                try:
                    heure, indicateurs = recuperer_donnees(symbole, API_KEY)
                    high, low = opr_range[symbole]
                    signal = generer_signal_opr(symbole, heure, indicateurs, high, low)
                    if signal and "aucune" not in signal.lower() and "pas de cassure" not in signal.lower():
                        await envoyer_message(f"📈 Signal OPR {symbole} ({heure})\n{signal}")
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] ❌ Pas de cassure OPR sur {symbole}", flush=True)
                except Exception as e:
                    print(f"❌ Erreur OPR {symbole} : {e}", flush=True)

# Enregistrement du range OPR à 15h45
async def memoriser_range_opr():
    print(f"[{time.strftime('%H:%M:%S')}] 📊 Enregistrement du range OPR", flush=True)
    for symbole in ["BTC/USD", "XAU/USD"]:
        try:
            heure, indicateurs = recuperer_donnees(symbole, API_KEY)
            # Extraction HIGH/LOW brut depuis les données
            high = None
            low = None
            match_high = re.search(r"High[^0-9]*([\d\.]+)", indicateurs)
            match_low = re.search(r"Low[^0-9]*([\d\.]+)", indicateurs)
            if match_high:
                high = float(match_high.group(1))
            if match_low:
                low = float(match_low.group(1))
            if high and low:
                opr_range[symbole] = (high, low)
                print(f"✅ Range OPR mémorisé pour {symbole} : High={high} / Low={low}", flush=True)
        except Exception as e:
            print(f"❌ Erreur lors de l’enregistrement du range OPR pour {symbole} : {e}", flush=True)

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

async def boucle_schedule():
    while True:
        schedule.run_pending()
        print(f"🕒 {time.strftime('%H:%M:%S')} - En attente de la prochaine exécution...", flush=True)
        await asyncio.sleep(1)

async def main():
    print("✅ Bot lancé. Démarrage des premières analyses...", flush=True)
    run_async(analyser_opportunites)
    schedule.every(5).minutes.do(lambda: run_async(analyser_opportunites))
    schedule.every().hour.at(":00").do(lambda: run_async(analyser_globale))
    schedule.every().day.at("15:45").do(lambda: run_async(memoriser_range_opr))
    schedule.every(1).minutes.do(lambda: run_async(analyser_opr))
    await boucle_schedule()

if __name__ == "__main__":
    asyncio.run(main())
