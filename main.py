import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees, analyser_tendance
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

async def verifier_et_envoyer_signal():
    bot = Bot(token=TOKEN)
    maintenant = datetime.now(pytz.timezone("Europe/Paris"))
    heure_actuelle = maintenant.hour + maintenant.minute / 60
    heure_str = maintenant.strftime("%H:%M")

    for symbole, (heure_debut, heure_fin) in SYMBOLS.items():
        try:
            if not (heure_debut <= heure_actuelle <= heure_fin):
                continue

            donnees = recuperer_donnees(symbole)
            tendance = analyser_tendance(symbole, donnees)
            contexte = contexte_macro_simplifie()

            message = generer_signal_ia(
                symbole,
                donnees,
                tendance,
                heure_str,
                contexte
            )

            if message and isinstance(message, str):
                await bot.send_message(chat_id=CHAT_ID, text=message)

        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbole} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)  # 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
