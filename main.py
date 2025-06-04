import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    for actif, infos in SYMBOLS.items():
        try:
            donnees = recuperer_donnees(actif, infos["twelve_symbol"])
            signal = generer_signal_ia(donnees)
            if signal:
                await bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)  # 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
