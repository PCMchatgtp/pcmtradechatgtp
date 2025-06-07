import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def analyser_et_envoyer():
    for symbole, nom_affichage in SYMBOLS.items():
        try:
            print(f"Analyse de {symbole}...")
            donnees = recuperer_donnees(symbole)
            signal = generer_signal_ia(symbole, donnees)
            if signal:
                await bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbole} : {e}")

async def boucle_analyse():
    while True:
        await analyser_et_envoyer()
        await asyncio.sleep(300)  # 5 minutes

if __name__ == "__main__":
    asyncio.run(boucle_analyse())