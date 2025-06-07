import openai
import os

def generer_signal_ia(symbole, donnees, heure, indicateurs):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    dernier_cours = donnees[0]["close"]

    prompt = f"""
Tu es un analyste financier IA. Voici les données pour {symbole} :
- Heure : {heure}
- Cours actuel : {dernier_cours}
- Moyenne des clôtures : {indicateurs['close_moyenne']}
- Volume moyen : {indicateurs['volume_moyen']}

Donne une analyse simple avec une opportunité de trade (achat ou vente), un stop, un TP1 et un taux de confiance estimé entre 0 et 100%.
"""

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message["content"]