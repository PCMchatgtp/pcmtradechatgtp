import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS, TWELVE_DATA_API_KEY
from market_data import recuperer_donnees, analyser_tendance
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    paris_tz = pytz.timezone('Europe/Paris')
    heure_actuelle = datetime.now(paris_tz).time()

    for symbole, meta in SYMBOLS.items():
        try:
            cours = recuperer_donnees(meta["twelve"], TWELVE_DATA_API_KEY)
            tendance = analyser_tendance(cours)
            heure = datetime.now(paris_tz).strftime("%H:%M")
            analyse = generer_signal_ia(symbole, cours, tendance, heure)

            await bot.send_message(chat_id=CHAT_ID, text=f"📊 Analyse pour {meta['nom']} :\n{analyse}")
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbole} : {e}")

if __name__ == "__main__":
    asyncio.run(verifier_et_envoyer_signal())
