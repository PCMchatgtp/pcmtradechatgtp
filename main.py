import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia
from datetime import datetime, time
import pytz

def est_dans_horaire(actif):
    paris = pytz.timezone("Europe/Paris")
    maintenant = datetime.now(paris).time()

    if actif == "XAUUSD":
        return time(7, 0) <= maintenant <= time(22, 0)
    elif actif == "NASDAQ":
        return time(15, 30) <= maintenant <= time(18, 0)
    return False

def analyser_conditions(signal):
    return signal.get("decision") == "prendre position"

async def verifier_et_envoyer_signal(bot):
    for actif in SYMBOLS:
        try:
            if not est_dans_horaire(actif):
                continue

            donnees = recuperer_donnees(actif)
            contexte = contexte_macro_simplifie()
            signal = generer_signal_ia(donnees, contexte)

            if analyser_conditions(signal):
                message = (
                    f"📡 Signal pour {actif} :\n\n"
                    f"📊 Analyse IA\n"
                    f"Actif : {actif}\n"
                    f"Prix actuel : {donnees['prix']}\n"
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
    bot = Bot(token=TOKEN)
    while True:
        await verifier_et_envoyer_signal(bot)
        await asyncio.sleep(300)  # 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
