
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(actif, donnees, tendance, heure, contexte_macro):
    prompt = f"""
Tu es un assistant de trading algorithmique.

Actif : {actif}
Tendance actuelle : {tendance}
Heure : {heure}
Contexte macroéconomique : {contexte_macro}
Données de marché brutes : {donnees}

Sur la base de ces éléments, indique :
1. S'il y a une opportunité de trade (achat, vente ou rien).
2. Le point d'entrée proposé.
3. Le stop loss conseillé.
4. Un ou plusieurs take profit (TP1, TP2, TP3 max).
5. Une estimation de probabilité de réussite du trade.

Si aucune opportunité n'est pertinente, réponds clairement qu'aucun trade ne doit être pris.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Erreur GPT : {e}"
