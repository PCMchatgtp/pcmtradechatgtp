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
opr_range = {}

# 🔁 Analyse toutes les 5 min
async def analyser_opportunites():
    print(f"[{time.strftime('%H:%M:%S')}] 🔄 Analyse des opportunités lancée", flush=True)
    symboles = SYMBOLS.split(",")
    for symbole in symboles:
        symbole = symbole.strip()
        print(f"➡️ Analyse en cours sur {symbole}", flush=True)
        try:
            heure, indicateurs = recuperer_donnees(symbole, API_KEY)
            analyse = generer_signal_ia(symbole, heure, indicateurs)

            if not analyse or "aucune opportunité" in analyse.lower():
                print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Aucune opportunité détectée sur {symbole}", flush=True)
                continue

            if "taux de réussite" in analyse.lower() and "%" in analyse:
                taux = re.search(r"(\d{1,3})\s*%", analyse)
                if taux and int(taux.group(1)) >= 60:
                    print(f"✅ Envoi du signal Telegram pour {symbole}", flush=True)
                    await asyncio.wait_for(
                        envoyer_message(f"💡 Opportunité détectée sur {symbole} ({heure})\n{analyse}"), timeout=10
                    )
                else:
                    print(f"❌ Taux de réussite trop faible sur {symbole}", flush=True)

        except asyncio.TimeoutError:
            print(f"⏱️ Timeout sur {symbole} – Telegram trop lent", flush=True)
        except Exception as e:
            print(f"❌ Erreur sur {symbole} : {e}", flush=True)

# 📈 OPR : prise de décision entre 15h45 et 16h15
async def analyser_opr():
    paris_tz = pytz.timezone("Europe/Paris")
    now = datetime.now(paris_tz)
    heure_now = now.strftime("%H:%M")
    heure_int = int(now.strftime("%H%M"))

    if 1545 <= heure_int <= 1615:
        for symbole in ["BTC/USD", "XAU/USD"]:
            if symbole in opr_range:
                try:
                    print(f"🔍 Analyse OPR pour {symbole}", flush=True)
                    heure, indicateurs = recuperer_donnees(symbole, API_KEY)
                    high, low = opr_range[symbole]
                    signal = generer_signal_opr(symbole, heure, indicateurs, high, low)

                    if signal and "aucune" not in signal.lower() and "pas de cassure" not in signal.lower():
                        await envoyer_message(f"📈 Signal OPR {symbole} ({heure})\n{signal}")
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] ❌ Pas de cassure OPR sur {symbole}", flush=True)
                except Exception as e:
                    print(f"❌ Erreur OPR {symbole} : {e}", flush=True)

# 🕔 Capture du range OPR à
