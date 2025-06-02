import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID
from market_data import recuperer_donnees
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

actifs = ["XAUUSD", "DAX", "NASDAQ"]  # Liste des actifs à analyser

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    contexte = contexte_macro_simplifie()
    for actif in actifs:
        try:
            donnees = recuperer_donnees(actif)
            signal = generer_signal_ia(donnees, contexte)

            message = (
                f"📡 Signal pour {actif} :\n\n"
                f"📊 Analyse IA\n"
                f"Actif : {donnees['actif']}\n"
                f"Prix actuel : {donnees['prix']}\n"
                f"Contexte macro : {contexte}\n\n"
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
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)  # 5 minutes entre chaque analyse

if __name__ == "__main__":
    asyncio.run(main())
