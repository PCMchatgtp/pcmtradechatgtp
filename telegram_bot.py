import aiohttp
import asyncio
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

async def envoyer_message(message: str):
    """
    Envoie un message Telegram uniquement si le message n’est pas vide.
    """
    if not message.strip():
        print("🔕 Message vide ignoré – rien à envoyer à Telegram")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as resp:
                if resp.status != 200:
                    print(f"❌ Erreur Telegram {resp.status}: {await resp.text()}")
                else:
                    print("📤 Message Telegram envoyé avec succès")

    except asyncio.TimeoutError:
        print("⏱️ Timeout lors de l’envoi Telegram")

    except Exception as e:
        print(f"❌ Exception lors de l’envoi Telegram : {e}")
