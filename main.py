import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from config import TOKEN, CHAT_ID
from market_data import recuperer_donnees
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

derniers_signaux = {}

actifs = ["XAUUSD", "DAX", "NASDAQ"]

async def verifier_et_envoyer_signal():
    bot = Bot(token=TOKEN)

    for actif in actifs:
        try:
            donnees = recuperer_donnees(actif)
            contexte = contexte_macro_simplifie()
            signal = generer_signal_ia(donnees, contexte)

            entree = signal["entree"]
            stop = signal["stop"]
            tp1 = signal["tp1"]
            tp2 = signal["tp2"]
            tp3 = signal["tp3"]
            macro = signal.get("macro", "")

            message = f"""📡 Signal pour {actif} :

📊 Analyse IA
Actif : {actif}
Prix actuel : {entree}
Contexte macro : {macro}

🔁 Entrée : {entree}
📉 Stop : {stop}
📈 TP1 : {tp1}
📈 TP2 : {tp2}
📈 TP3 : {tp3}
🎯 Break-even après TP1 atteint."""

            await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)

        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    await verifier_et_envoyer_signal()

if __name__ == "__main__":
    asyncio.run(main())
