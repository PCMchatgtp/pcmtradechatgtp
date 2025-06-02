import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID
from market_data import recuperer_donnees
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    actifs = ["BTCUSD", "XAUUSD", "NASDAQ", "DAX"]
    for actif in actifs:
        try:
            donnees = recuperer_donnees(actif)
            contexte = contexte_macro_simplifie()
            signal = generer_signal_ia(donnees, contexte)

            if "Pas d'entrée" not in signal:
                await bot.send_message(chat_id=CHAT_ID, text=f"📡 Signal pour *{actif}* :\n\n{signal}", parse_mode="Markdown")
            else:
                print(f"[INFO] Aucun signal pour {actif}")
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
