import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID
from market_data import recuperer_donnees
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

actifs = ["XAUUSD", "DAX", "NASDAQ"]

async def verifier_et_envoyer_signal():
    for actif in actifs:
        try:
            donnees = recuperer_donnees(actif)
            contexte = contexte_macro_simplifie()
            signal = generer_signal_ia(donnees, contexte)
            message = (
                f"📡 Signal pour {actif} :\n\n"
                f"📊 Analyse IA\n"
                f"Actif : {signal['actif']}\n"
                f"Prix actuel : {signal['prix']}\n"
                f"Contexte macro : {signal['macro']}\n\n"
                f"🔁 Entrée : {signal['entree']}\n"
                f"📉 Stop : {signal['stop']}\n"
                f"📈 TP1 : {signal['tp1']}\n"
                f"📈 TP2 : {signal['tp2']}\n"
                f"📈 TP3 : {signal['tp3']}\n"
                f"🎯 Break-even après TP1 atteint."
            )
            await bot.send_message(chat_id=CHAT_ID, text=message)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    await verifier_et_envoyer_signal()

if __name__ == "__main__":
    asyncio.run(main())
