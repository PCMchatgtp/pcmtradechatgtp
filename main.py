import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

def verifier_et_envoyer_signal():
    bot = Bot(token=TOKEN)
    contexte = contexte_macro_simplifie()

    for actif in SYMBOLS:
        try:
            donnees = recuperer_donnees(actif)
            signal = generer_signal_ia(donnees, contexte)

            message = (
                f"📡 Signal pour {signal['actif']} :\n\n"
                f"📊 Analyse IA\n"
                f"Actif : {signal['actif']}\n"
                f"Prix actuel : {signal['prix']}\n"
                f"Contexte macro : {signal['macro']}\n\n"
                f"🔁 Entrée : {signal['prix']}\n"
                f"📉 Stop : {signal['stop']}\n"
                f"📈 TP1 : {signal['tp1']}\n"
                f"📈 TP2 : {signal['tp2']}\n"
                f"📈 TP3 : {signal['tp3']}\n"
                f"{signal['break_even']}"
            )

            bot.send_message(chat_id=CHAT_ID, text=message)

        except Exception as e:
            bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

if __name__ == "__main__":
    verifier_et_envoyer_signal()
