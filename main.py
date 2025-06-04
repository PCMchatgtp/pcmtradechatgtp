import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees, analyser_tendance
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia
from datetime import datetime
import pytz

bot = Bot(token=TOKEN)

def heure_locale():
    tz = pytz.timezone("Europe/Paris")
    return datetime.now(tz).strftime("%H:%M")

async def verifier_et_envoyer_signal():
    for actif in SYMBOLS:
        try:
            donnees = recuperer_donnees(actif)
            tendance = analyser_tendance(donnees)
            heure = heure_locale()
            contexte = contexte_macro_simplifie()
            signal = generer_signal_ia(donnees, tendance, heure, contexte)
            await bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"Erreur sur {actif} : {e}")

async def main():
    await verifier_et_envoyer_signal()

if __name__ == "__main__":
    asyncio.run(main())
