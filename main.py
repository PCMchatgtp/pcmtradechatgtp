from config import OPENAI_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS
from telegram_bot import envoyer_message
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
import time
import datetime
import pytz

def analyse_globale():
    resume = []
    paris_tz = pytz.timezone("Europe/Paris")
    maintenant = datetime.datetime.now(paris_tz).strftime("%Y-%m-%d %H:%M:%S")
    for symbole in SYMBOLS:
        try:
            donnees, heure, indicateurs = recuperer_donnees(symbole)
            signal = generer_signal_ia(symbole, donnees, heure, indicateurs)
            envoyer_message(f"💡 {symbole}\n\n{signal}")
            resume.append(f"✅ {symbole}")
        except Exception as e:
            resume.append(f"❌ {symbole} : {str(e)}")
    envoyer_message(f"📊 Analyse globale {maintenant}\n" + "\n".join(resume))

if __name__ == "__main__":
    analyse_globale()