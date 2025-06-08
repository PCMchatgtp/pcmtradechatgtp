from config import OPENAI_API_KEY
from gpt_prompt import generer_signal_ia
from market_data import recuperer_donnees
from telegram_bot import envoyer_message
import time
import pytz
from datetime import datetime
from config import SYMBOLS, TELEGRAM_BOT_TOKEN

print("✅ Imports réussis et clé OpenAI chargée :", bool(OPENAI_API_KEY))

def boucle_analyse():
    paris_tz = pytz.timezone('Europe/Paris')
    maintenant = datetime.now(paris_tz)
    heure = maintenant.strftime("%H:%M")

    for symbole in SYMBOLS:
        try:
            data = recuperer_donnees(symbole)
            if not data:
                raise ValueError("❌ Données manquantes.")
            signal, commentaire, proba = generer_signal_ia(symbole, heure, data)
            envoyer_message(f"💡 {symbole} analysé avec succès.")
        except Exception as e:
            envoyer_message(f"❌ Erreur sur {symbole} : {e}")

if __name__ == '__main__':
    boucle_analyse()
