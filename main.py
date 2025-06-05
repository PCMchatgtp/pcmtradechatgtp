import asyncio
from datetime import datetime
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

derniers_signaux = {}

async def verifier_et_envoyer_signal():
    bot = Bot(token=TOKEN)

    for symbole, nom in SYMBOLS.items():
        try:
            donnees = recuperer_donnees(symbole)
            heure = datetime.utcnow().hour

            if symbole == "XAUUSD" and not (7 <= heure <= 22):
                continue
            if symbole == "BTCUSD" and not (7 <= heure <= 22):
                continue

            signal = generer_signal_ia(donnees, heure)

            if signal and signal != derniers_signaux.get(symbole):
                await bot.send_message(chat_id=CHAT_ID, text=f"🔔 Signal détecté sur {nom} :\n\n{signal}")
                derniers_signaux[symbole] = signal

        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {nom} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
