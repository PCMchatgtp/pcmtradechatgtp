from telegram import Bot
import asyncio
import os
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

# Création d'un bot global unique
bot = Bot(token=TELEGRAM_TOKEN)

async def envoyer_message(message):
    try:
        # Utilisation d'une session temporaire asynchrone
        await asyncio.create_task(bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message))
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi Telegram : {e}", flush=True)
