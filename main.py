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

            # Timeout pour bloquer max 20s si GPT plante
            analyse = await asyncio.wait_for(
                generer_signal_ia(symbole, heure, indicateurs), timeout=20
            )

            if not analyse or "aucune opportunité" in analyse.lower():
                print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Aucune opportunité détectée sur {symbole}", flush=True)
                continue

            if "taux de réussite" in analyse.lower() and "%" in analyse:
                taux = re.search(r"(\d{1,3})\s*%", analyse)
                if taux and int(taux.group(1)) >= 60:
                    # Timeout aussi pour Telegram
                    await asyncio.wait_for(
                        envoyer_message(f"💡 Opportunité détectée sur {symbole} ({heure})\n{analyse}"), timeout=10
                    )

        except asyncio.TimeoutError:
            print(f"⏱️ Timeout sur {symbole} – GPT ou Telegram trop lent", flush=True)
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
            await asyncio.wait_for(
                generer_signal_ia(symbole, heure, indicateurs), timeout=20
            )
            resume_global += f"✅ {symbole}\n"
        except asyncio.TimeoutError:
            resume_global += f"❌ {symbole} : Timeout GPT\n"
        except Exception as e:
            resume_global += f"❌ {symbole} : {e}\n"
    await envoyer_message(resume_global)

# Wrapper sécurisé
def run_async(coroutine_func):
    loop = asyncio.get_event_loop()
    coroutine = coroutine_func()  # ✅ Appel de la fonction pour créer la coroutine

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
    await boucle_schedule()

if __name__ == "__main__":
    asyncio.run(main())
