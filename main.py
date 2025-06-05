import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    for symbole in SYMBOLS:
        try:
            donnees = recuperer_donnees(symbole)
            if donnees is None:
                continue
            message = generer_signal_ia(donnees)
            if message:
                await bot.send_message(chat_id=CHAT_ID, text=message)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbole} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())