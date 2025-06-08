from config import OPENAI_API_KEY, TOKEN, CHAT_ID, SYMBOLS
from market_data import recuperer_donnees
from gpt_prompt import generer_signal_ia
import asyncio
import datetime
from telegram_bot import envoyer_message

print("✅ Imports réussis et clé OpenAI chargée :", bool(OPENAI_API_KEY))

async def analyse_marche():
    erreurs = []
    actifs = SYMBOLS.split(",")

    for symbole in actifs:
        try:
            donnees, heure, indicateurs = recuperer_donnees(symbole)
            signal = generer_signal_ia(symbole, donnees, heure, indicateurs)
            await envoyer_message(f"💡 {symbole} : {signal}")
        except Exception as e:
            erreurs.append(f"❌ {symbole} : {str(e)}")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    synthese = f"📊 Analyse globale {now}\n"
    synthese += "\n".join(erreurs) if erreurs else "✅ Tout fonctionne normalement."
    await envoyer_message(synthese)

if __name__ == "__main__":
    asyncio.run(analyse_marche())