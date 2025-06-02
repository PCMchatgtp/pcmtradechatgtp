import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from config import TOKEN, CHAT_ID
from market_data import recuperer_donnees
from macro_context import contexte_macro_simplifie
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)
derniers_signaux = {}

# Fuseau horaire Europe/Paris
paris = pytz.timezone("Europe/Paris")

async def verifier_et_envoyer_signal():
    actifs = {
        "NASDAQ": (15, 16),
        "DAX": (9, 10),
        "XAUUSD": (0, 24)
    }

    maintenant = datetime.now(paris)
    heure_actuelle = maintenant.hour

    for actif, (heure_debut, heure_fin) in actifs.items():
        if heure_debut <= heure_actuelle <= heure_fin:
            try:
                donnees = recuperer_donnees(actif)
                contexte = contexte_macro_simplifie()
                signal = generer_signal_ia(donnees, contexte)

                # Empêcher les doublons
                if signal != derniers_signaux.get(actif):
                    await bot.send_message(chat_id=CHAT_ID, text=signal)
                    derniers_signaux[actif] = signal
            except Exception as e:
                await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)  # toutes les 5 min

if __name__ == "__main__":
    asyncio.run(main())
