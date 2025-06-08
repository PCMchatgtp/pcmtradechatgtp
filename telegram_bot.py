import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def envoyer_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    if not response.ok:
        raise Exception("❌ Échec de l'envoi Telegram : " + response.text)