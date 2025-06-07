import asyncio
from datetime import datetime
from telegram import Bot
from config import TOKEN, CHAT_ID, SYMBOLS, twelve_data_api_key, OPENAI_API_KEY
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia

bot = Bot(token=TOKEN)
etat_analyse = {}

async def analyser_et_envoyer():
    while True:
        maintenant = datetime.now()
        heure = maintenant.strftime('%H:%M')
        minute = maintenant.minute

        messages_resume = []
        for symbole in SYMBOLS:
            try:
                print(f"Analyse de {symbole}...")
                donnees, indicateurs = recuperer_donnees(symbole, twelve_data_api_key)
                plan = generer_signal_ia(symbole, donnees, heure, indicateurs)
                await bot.send_message(chat_id=CHAT_ID, text=plan)
                etat_analyse[symbole] = "✅ OK"
            except Exception as e:
                msg = f"❌ Erreur sur {symbole} : {str(e)}"
                await bot.send_message(chat_id=CHAT_ID, text=msg)
                etat_analyse[symbole] = f"❌ {str(e)}"

        if minute == 0:
            resume = f"🕒 Résumé à {heure}\n"
            for symbole, etat in etat_analyse.items():
                resume += f"{symbole} : {etat}\n"
            await bot.send_message(chat_id=CHAT_ID, text=resume)

        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(analyser_et_envoyer())