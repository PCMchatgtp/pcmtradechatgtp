import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from signal_loop import verifier_et_envoyer_signal
from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)

async def start(update, context):
    await update.message.reply_text("Bot de signaux IA actif.")

async def post_init(app):
    app.create_task(verifier_et_envoyer_signal(app.bot))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
