
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generer_signal_ia(donnees, heure, contexte_macro):
    try:
        prompt = f"""
Tu es un assistant expert en scalping sur les marchés financiers.
Voici les données du marché :

Actif : {donnees['actif']}
Prix actuel : {donnees['prix']}
Heure : {heure}h
Contexte macroéconomique : {contexte_macro["résumé"]}

Ta tâche est de déterminer s'il y a une opportunité de trade à court terme (scalping), uniquement si la probabilité de réussite est élevée.

Tu dois répondre uniquement dans ce format :
---
Sens du trade : Achat / Vente / Aucun
Entrée : [prix]
Stop : [prix]
TP1 : [prix]
TP2 : [prix facultatif]
TP3 : [prix facultatif]
Commentaire : [explication concise]
---
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Erreur GPT : {e}"
