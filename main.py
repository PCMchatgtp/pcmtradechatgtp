
import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

def verifier_et_envoyer_signal():
    bot = Bot(token=TOKEN)
    paris_tz = pytz.timezone('Europe/Paris')
    maintenant = datetime.now(paris_tz)
    heure = maintenant.hour
    minute = maintenant.minute

    for actif in SYMBOLS:
        # Plage horaire spécifique
        if actif == "NASDAQ" and (heure < 15 or (heure == 15 and minute < 30) or heure >= 18):
            continue
        if actif == "XAUUSD" and (heure < 7 or heure > 22):
            continue

        try:
            donnees = recuperer_donnees(actif)
            contexte = contexte_macro_simplifie()
            signal = generer_signal_ia(donnees, contexte)
            bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    while True:
        verifier_et_envoyer_signal()
        await asyncio.sleep(300)  # Toutes les 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
