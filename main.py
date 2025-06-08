
import time
import pytz
from datetime import datetime
from config import OPENAI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TWELVE_DATA_API_KEY, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
from telegram import Bot

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def envoyer_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Erreur lors de l'envoi du message Telegram : {e}")

def analyse_complete():
    erreurs = []
    for symbole in SYMBOLS:
        try:
            maintenant = datetime.now(pytz.timezone("Europe/Paris"))
            donnees, indicateurs = recuperer_donnees(symbole, TWELVE_DATA_API_KEY)
            commentaire, plan = generer_signal_ia(symbole, maintenant.strftime("%H:%M"), indicateurs)
            if plan:
                envoyer_message(f"💡 {symbole}
{commentaire}
{plan}")
        except Exception as e:
            erreurs.append(f"{symbole} : {e}")
    return erreurs

if __name__ == "__main__":
    while True:
        erreurs = analyse_complete()
        if erreurs:
            resume = "⚠️ Résumé : erreurs détectées sur :
" + "
".join(erreurs)
        else:
            resume = "✅ Résumé : tout fonctionne normalement."
        envoyer_message(resume)
        time.sleep(300)  # toutes les 5 minutes
