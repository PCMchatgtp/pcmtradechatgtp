import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generer_signal_ia(donnees, macro="Aucune donnée macro disponible."):
    actif = donnees["actif"]
    prix = donnees["prix"]

    prompt = f"""
Tu es un assistant de trading scalping. Analyse cet actif : {actif}.
Prix actuel : {prix}
Contexte macro : {macro}

Règles :
- Ne propose une entrée que s’il y a une réelle opportunité selon ton analyse technique (support/résistance, impulsion, cassure…).
- Timeframe : 5 minutes, pas de swing.
- Objectif : signal rentable avec TP1 > SL.
- Réponds avec Entrée, Stop, TP1, TP2, TP3.

S'il n'y a **aucune opportunité claire**, réponds uniquement : "Aucune opportunité".
"""

    reponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    texte = reponse.choices[0].message.content.strip()
    return texte
