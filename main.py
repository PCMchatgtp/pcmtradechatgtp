import asyncio
from datetime import datetime
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
import json

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    heure = datetime.now().hour
    actifs = {
        "XAUUSD": (7, 22),
        "BTCUSD": (7, 22),
        "NASDAQ": (15, 18)
    }

    for actif, (heure_debut, heure_fin) in actifs.items():
        if not (heure_debut <= heure <= heure_fin):
            continue

        try:
            donnees = recuperer_donnees(actif)
            contexte_macro = "Marché calme, pas d'annonces majeures."
            signal = generer_signal_ia(donnees, contexte_macro)

            resultat = json.loads(signal)

            if resultat.get("opportunite") is True:
                plan = resultat["plan"]
                message = (
                    f"Signal pour {actif} :\n\n"
                    f"Analyse IA\n"
                    f"Actif : {resultat['actif']}\n"
                    f"Prix : {resultat['prix']}\n"
                    f"Tendance : {resultat['tendance']}\n"
                    f"Contexte macro : {resultat['contexte_macro']}\n\n"
                    f"Entrée : {plan['entree']}\n"
                    f"Stop : {plan['stop']}\n"
                    f"TP1 : {plan['tp1']}\n"
                    f"TP2 : {plan['tp2']}\n"
                    f"TP3 : {plan['tp3']}\n"
                    f"Heure : {resultat['heure']}"
                )
                await bot.send_message(chat_id=CHAT_ID, text=message)

        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"Erreur sur {actif} : {e}")

async def main():
    while True:
        await verifier_et_envoyer_signal()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())