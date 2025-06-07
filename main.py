
import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, TWELVE_DATA_API_KEY, OPENAI_API_KEY
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

SYMBOLS = {
    "XAUUSD": "XAU/USD",
    "BTCUSD": "BTC/USD",
    "QQQ": "NASDAQ"
}

bot = Bot(token=TOKEN)

async def analyse_et_envoi():
    for symbole, nom_affiche in SYMBOLS.items():
        try:
            donnees = recuperer_donnees(symbole, TWELVE_DATA_API_KEY)
            signal = generer_signal_ia(symbole, donnees['heure'], donnees['indicateurs'], OPENAI_API_KEY)
            await bot.send_message(chat_id=CHAT_ID, text=signal)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {nom_affiche} : {e}")

asyncio.run(analyse_et_envoi())
