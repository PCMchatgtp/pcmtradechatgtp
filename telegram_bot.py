from telegram import Bot
from config import TOKEN, CHAT_ID

bot = Bot(token=TOKEN)

async def envoyer_message(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)