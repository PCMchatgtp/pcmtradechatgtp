import asyncio
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)

async def verifier_signaux():
    for symbole, nom_affichage in SYMBOLS.items():
        try:
            donnees, heure, indicateurs = recuperer_donnees(symbole)
            plan, commentaire = generer_signal_ia(symbole, donnees, heure, indicateurs)
            if plan:
                await bot.send_message(chat_id=CHAT_ID, text=f"✅ Signal détecté pour {nom_affichage} :\n{plan}\n\n{commentaire}")
        except Exception as e:
            await bot.send_message(chat_id=CHAT_ID, text=f"❌ Erreur sur {nom_affichage} : {e}")

async def boucle():
    while True:
        await verifier_signaux()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(boucle())
