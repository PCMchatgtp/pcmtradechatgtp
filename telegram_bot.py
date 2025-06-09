from telegram import Bot
from telegram.constants import ParseMode
from telegram.request import HTTPXRequest
import asyncio
import os
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

# Crée un bot avec une gestion de pool propre via HTTPX (plus fiable que aiohttp par défaut)
request = HTTPXRequest(connect_timeout=5, read_timeout=10)
bot = Bot(token=TELEGRAM_TOKEN, request=request)

async def envoyer_message(message):
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode=ParseMode.MARKDOWN  # optionnel, pour styliser si besoin
        )
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi Telegram : {e}", flush=True)
