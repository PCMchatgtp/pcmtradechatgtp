import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from config import TOKEN, CHAT_ID, TWELVE_DATA_API_KEY
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

SYMBOLS = {
    "XAU/USD": "XAU/USD",
    "BTC/USD": "BTC/USD",
    "QQQ": "QQQ"
}

async def envoyer_signal(symbol, data):
    try:
        heure = datetime.now(pytz.timezone("Europe/Paris")).strftime("%H:%M")
        message = generer_signal_ia(symbol, heure, data)
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbol} : {e}")

async def main():
    for symbol in SYMBOLS:
        try:
            data = recuperer_donnees(SYMBOLS[symbol], TWELVE_DATA_API_KEY)
            await envoyer_signal(symbol, data)
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbol} : {e}")

asyncio.run(main())