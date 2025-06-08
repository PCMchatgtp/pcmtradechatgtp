import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(symbole, donnees, heure, indicateurs):
    prompt = f"""
Analyse le marché {symbole} à {heure} avec les données suivantes :
- Open : {indicateurs['open']}
- High : {indicateurs['high']}
- Low : {indicateurs['low']}
- Close : {indicateurs['close']}
- Volume : {indicateurs['volume']}

Donne une recommandation claire :
- Prise de position ou non
- Direction (achat ou vente)
- Niveau d'entrée, stop, TP1, TP2, TP3
- Contexte de la décision
"""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message["content"].strip()