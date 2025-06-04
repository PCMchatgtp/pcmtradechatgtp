import asyncio
from datetime import datetime
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

derniers_signaux = {}

def est_dans_fenetre_trading(actif):
    now = datetime.now()
    heure = now.hour + now.minute / 60

    if actif == "XAUUSD":
        return 7 <= heure <= 22
    elif actif == "NASDAQ":
        return 15.5 <= heure <= 18
    return False

async def verifier_et_envoyer_signal():
    bot = Bot(token=TOKEN)

    for actif in SYMBOLS.keys():
        if not est_dans_fenetre_trading(actif):
            continue

        try:
            donnees = recuperer_donnees(actif)
            signal = generer_signal_ia(donnees)

            if "Aucune opportunité" in signal:
                continue

            message = f"📡 Signal pour {actif} :\n\n{signal}"
            if derniers_signaux.get(actif) != message:
                await bot.send_message(chat_id=CHAT_ID, text=message)
                derniers_signaux[actif] = message

        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)  # Toutes les 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
