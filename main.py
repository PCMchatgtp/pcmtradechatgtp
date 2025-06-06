import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def analyse_marche():
    for symbole in SYMBOLS:
        print(f"Analyse de {symbole}...")
        try:
            donnees = recuperer_donnees(symbole)
            if donnees is None:
                raise ValueError("❌ Données manquantes")
            signal = generer_signal_ia(symbole, donnees)
            if signal:
                await bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbole} : {e}")

async def boucle():
    while True:
        await analyse_marche()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(boucle())