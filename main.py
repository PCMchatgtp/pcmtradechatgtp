
import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def verifier_et_envoyer_signal():
    for symbole, actif_info in SYMBOLS.items():
        try:
            print(f"Analyse de {symbole}...")
            donnees = recuperer_donnees(symbole)
            if not donnees:
                raise ValueError(f"❌ Données invalides pour {symbole}")

            tendance = donnees["tendance"]
            heure = donnees["heure"]
            prix = donnees["prix"]
            volume = donnees["volume"]
            rsi = donnees["rsi"]
            ema = donnees["ema"]
            macd = donnees["macd"]

            message = generer_signal_ia(symbole, tendance, heure, prix, volume, rsi, ema, macd)
            await bot.send_message(chat_id=CHAT_ID, text=message)

        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {symbole} : {e}")

asyncio.run(verifier_et_envoyer_signal())
