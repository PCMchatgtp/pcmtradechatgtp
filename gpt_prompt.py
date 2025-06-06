import openai
from datetime import datetime

def generer_signal_ia(symbole, cours, tendance, heure):
    dernier_close = cours[0]["close"]
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""
Tu es un assistant de trading. Voici les informations de marché :
Symbole : {symbole}
Prix actuel : {dernier_close}
Tendance actuelle : {tendance}
Heure actuelle : {heure}

Analyse les données et indique s’il y a une opportunité de trade claire. Si oui, donne le sens (achat/vente), un point d’entrée, un stop loss, et deux take profits. Termine par une estimation du pourcentage de probabilité de succès.

Réponds de manière concise et exploitable immédiatement.
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"❌ Erreur GPT : {e}"
