import asyncio
from config import TOKEN, CHAT_ID, SYMBOLS, twelve_data_api_key
from telegram import Bot
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    for symbole in SYMBOLS:
        try:
            print(f"Analyse de {symbole}...")
            donnees = recuperer_donnees(symbole, twelve_data_api_key)
            signal = generer_signal_ia(symbole, donnees)
            if signal:
                await bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbole} : {e}")

async def boucle():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)  # 5 minutes

if __name__ == "__main__":
    asyncio.run(boucle())