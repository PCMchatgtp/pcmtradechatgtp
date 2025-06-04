import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generer_signal_ia(symbole, donnees, tendance, heure, contexte_macro):
    prompt = f"""
Tu es un expert en trading à court terme sur les marchés financiers.
Ton rôle est d’analyser le marché de manière très rigoureuse et intelligente à partir des données suivantes pour détecter uniquement les opportunités de scalping ou day trading à forte probabilité.

Voici les données du marché :
Actif : {symbole}
Prix actuel : {donnees['prix']}
Heure : {heure}
Tendance : {tendance}

Voici le contexte macroéconomique à prendre en compte dans ton analyse :
{contexte_macro}

Ta tâche : 
- Déterminer s’il existe une opportunité de trade pertinente **à très court terme**.
- Si aucune opportunité claire et forte ne ressort, tu dois l’indiquer clairement : « Aucune opportunité pertinente actuellement. »
- Sinon, propose un plan structuré avec : sens du trade, point d’entrée, stop, TP1 et TP2.
- Ne propose jamais un trade si le ratio gain/risque sur TP1 est inférieur à 1:1.
- Utilise un ton synthétique et clair, pas de blabla inutile.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse de marché et stratégie de trading."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Erreur GPT : {e}"
