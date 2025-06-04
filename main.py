import asyncio
from datetime import datetime
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
import pytz

paris_tz = pytz.timezone('Europe/Paris')

async def verifier_et_envoyer_signal():
    bot = Bot(token=TOKEN)
    maintenant = datetime.now(paris_tz)

    for actif, infos in SYMBOLS.items():
        heure = maintenant.hour
        if not (infos["start_hour"] <= heure <= infos["end_hour"]):
            continue
        try:
            donnees = recuperer_donnees(actif, infos["symbol"])
            signal = generer_signal_ia(donnees)
            message = f"📡 Signal pour {actif} :\n\n📊 Analyse IA\nActif : {donnees['actif']}\nPrix actuel : {donnees['prix']}\n\n🔁 Entrée : {signal['entrée']}\n📉 Stop : {signal['stop']}\n📈 TP1 : {signal['tp1']}\n📈 TP2 : {signal['tp2']}\n📈 TP3 : {signal['tp3']}\n🎯 Break-even après TP1 atteint."
            await bot.send_message(chat_id=CHAT_ID, text=message)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {actif} : {e}")

async def main():
    await verifier_et_envoyer_signal()

if __name__ == "__main__":
    asyncio.run(main())