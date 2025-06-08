from config import OPENAI_API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS
from telegram_bot import envoyer_message
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
from datetime import datetime
import time
import pytz

def analyser_et_envoyer_signaux():
    erreurs = []
    for symbole in SYMBOLS:
        try:
            donnees, heure, indicateurs = recuperer_donnees(symbole.strip())
            plan = generer_signal_ia(symbole, donnees, heure, indicateurs)
            if plan:
                envoyer_message(f"📈 Signal détecté sur {symbole} :\n{plan}")
        except Exception as e:
            erreurs.append(f"❌ {symbole} : {e}")
    return erreurs

def envoyer_resume_global(erreurs):
    heure = datetime.now(pytz.timezone("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S")
    resume = f"📊 Analyse globale {heure}\n"
    for symbole in SYMBOLS:
        if any(symbole in err for err in erreurs):
            err_text = next(err for err in erreurs if symbole in err)
            resume += f"{err_text}\n"
        else:
            resume += f"✅ {symbole}\n"
    envoyer_message(resume)

if __name__ == "__main__":
    derniere_heure = None
    while True:
        erreurs = analyser_et_envoyer_signaux()
        heure_actuelle = datetime.now().hour
        if heure_actuelle != derniere_heure:
            envoyer_resume_global(erreurs)
            derniere_heure = heure_actuelle
        time.sleep(300)