from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

def envoyer_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)