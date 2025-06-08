from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

def envoyer_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Erreur Telegram : {e}")