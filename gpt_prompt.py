import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generer_signal_ia(donnees, heure):
    prix_actuel = float(donnees[0]["close"])
    prix_passe = [float(candle["close"]) for candle in donnees[1:]]

    tendance = "hausse" if prix_actuel > max(prix_passe) else "baisse"
    variation = prix_actuel - prix_passe[-1]

    prompt = f"""
Voici des données de marché en temps réel pour un actif. L'heure actuelle est {heure}h UTC.
- Tendance actuelle : {tendance}
- Prix actuel : {prix_actuel}
- Évolution récente : {variation:+.2f}

Génère un commentaire d'analyse technique comme si tu étais un expert en trading. Propose un plan de trade avec :
1. Sens (achat ou vente),
2. Niveau d'entrée,
3. Stop loss,
4. TP1 (objectif minimum),
5. Un taux de réussite estimé (en %),
6. Justification concise de l’opportunité.

Refuse de proposer un trade s’il n’y a pas d’opportunité réelle avec un bon risk:reward (TP1 - Entrée ≥ Entrée - Stop).
"""

    reponse = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    message = reponse.choices[0].message.content.strip()
    if "aucune opportunité" in message.lower():
        return None
    return message
