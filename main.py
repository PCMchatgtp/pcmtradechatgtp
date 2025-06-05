import os
import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS, TWELVE_DATE_API_KEY
from market_data import recuperer_donnees, analyser_tendance
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    heure_actuelle = datetime.now(pytz.timezone("Europe/Paris"))
    heure = heure_actuelle.strftime("%H:%M")
    actif_autorises = []

    if heure_actuelle.hour >= 7 and heure_actuelle.hour < 22:
        actif_autorises += ["XAUUSD", "BTCUSD"]
    if heure_actuelle.hour >= 15 and heure_actuelle.hour < 18:
        actif_autorises += ["NASDAQ"]

    for symbole in actif_autorises:
        try:
            donnees = recuperer_donnees(SYMBOLS[symbole], twelve_data_api_key)
            tendance = analyser_tendance(donnees)

            signal = generer_signal_ia(symbole, donnees["prix"], tendance, heure)

            if signal:
                await bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbole} : {e}")

async def boucle():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(boucle())
