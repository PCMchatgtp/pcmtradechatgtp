import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(symbole, donnees):
    dernier = donnees[0]
    texte = f"Voici les dernières données pour {symbole} :\n{dernier}"

    prompt = f"""
    Analyse technique basée sur : {texte}

    Donne uniquement s'il y a une opportunité de trade crédible.
    Réponds en précisant :
    - Le sens du trade (achat ou vente)
    - Le point d’entrée
    - Un stop
    - TP1, TP2
    - Un commentaire d’IA expliquant brièvement pourquoi, avec un pourcentage de fiabilité estimé.
    Ne propose rien si la configuration n’est pas claire.
    """

    reponse = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return reponse.choices[0].message["content"].strip()