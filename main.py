import time
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS, TWELVE_DATA_API_KEY, OPENAI_API_KEY
from telegram_notifier import envoyer_message
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

import datetime

def analyse():
    for symbole in SYMBOLS:
        try:
            maintenant = datetime.datetime.now().strftime("%H:%M")
            donnees, indicateurs = recuperer_donnees(symbole, TWELVE_DATA_API_KEY)
            message = generer_signal_ia(symbole, donnees, maintenant, indicateurs)
            envoyer_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, message)
        except Exception as e:
            envoyer_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, f"❌ Erreur sur {symbole} : {str(e)}")

if __name__ == "__main__":
    while True:
        analyse()
        time.sleep(300)