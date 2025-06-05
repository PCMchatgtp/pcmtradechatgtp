
import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees, analyser_tendance
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    for actif in SYMBOLS:
        try:
            symbole = SYMBOLS[actif]
            donnees = recuperer_donnees(symbole)
            tendance = analyser_tendance(donnees)
            heure = datetime.now(pytz.timezone("Europe/Paris")).strftime("%H:%M")
            contexte_macro = contexte_macro_simplifie()
            message = generer_signal_ia(
                actif=actif,
                donnees=donnees,
                tendance=tendance,
                heure=heure,
                contexte_macro=contexte_macro
            )
            if message:
                await bot.send_message(chat_id=CHAT_ID, text=message)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)  # toutes les 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
