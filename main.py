
import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS, OPENAI_API_KEY, TWELVE_DATA_API_KEY
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def analyser_et_envoyer():
    for symbole in SYMBOLS:
        try:
            print(f"Analyse de {symbole}...")
            donnees = recuperer_donnees(symbole, twelve_data_api_key)
            signal = generer_signal_ia(symbole, donnees, OPENAI_API_KEY)
            if signal:
                await bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbole} : {e}")

async def boucle_principale():
    while True:
        await analyser_et_envoyer()
        await asyncio.sleep(300)

if __name__ == '__main__':
    asyncio.run(boucle_principale())
