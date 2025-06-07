import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(symbole, donnees):
    dernier_cours = donnees[0]
    prompt = f"""
Tu es un expert en trading. Voici les dernières données de marché pour {symbole} :
{dernier_cours}

Analyse la tendance actuelle et dis s'il y a une opportunité de trade à très court terme.
Précise :
- Le sens du trade (achat ou vente)
- Un point d’entrée
- Un stop loss
- Un ou plusieurs take profit
- Un commentaire court expliquant la décision
- Un taux de probabilité de réussite estimé
"""

    reponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return reponse.choices[0].message["content"]