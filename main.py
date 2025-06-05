
import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees, actif_dans_horaire, heure_actuelle
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

derniers_signaux = {}

async def verifier_et_envoyer_signal():
    for actif in SYMBOLS:
        try:
            if not actif_dans_horaire(actif):
                continue

            donnees = recuperer_donnees(actif)
            heure = heure_actuelle()
            contexte = contexte_macro_simplifie()

            message = generer_signal_ia(donnees, heure, contexte)

            if "Aucun" in message or "aucune" in message.lower():
                continue

            if message != derniers_signaux.get(actif):
                await bot.send_message(chat_id=CHAT_ID, text=f"📊 {actif} \n{message}")
                derniers_signaux[actif] = message

        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
