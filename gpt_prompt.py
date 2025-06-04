
from openai import OpenAI

client = OpenAI()

def generer_signal_ia(actif, prix, tendance, heure, contexte_macro):
    prompt_utilisateur = f"""
Tu es un expert en trading algorithmique. Tu dois analyser un marché à partir des éléments suivants :

Actif : {actif}
Prix actuel : {prix}
Tendance détectée : {tendance}
Heure : {heure}
Contexte macro-économique : {contexte_macro}

Ta tâche est de dire s’il y a une opportunité de trade à court terme (scalping), et uniquement si c’est pertinent.
Si aucune opportunité claire ne se présente, réponds : "Aucune opportunité à ce moment."
Sinon, fournis un plan de trading avec :
- Direction (achat ou vente)
- Niveau d'entrée exact
- Stop loss
- Take profit 1, 2 et 3
- Justification rapide de la décision

Tu dois être précis, synthétique, et uniquement donner un signal si la configuration est nette.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un expert en analyse de marché et scalping."},
            {"role": "user", "content": prompt_utilisateur}
        ]
    )

    return response.choices[0].message.content
