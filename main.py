from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

def verifier_et_envoyer_signal():
    bot = Bot(token=TOKEN)
    for actif in SYMBOLS:
        try:
            donnees = recuperer_donnees(actif)
            contexte = contexte_macro_simplifie()
            signal = generer_signal_ia(donnees, contexte)
            bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

if __name__ == "__main__":
    verifier_et_envoyer_signal()
