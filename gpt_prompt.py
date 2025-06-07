
import openai

def generer_signal_ia(symbole, heure, indicateurs, openai_api_key):
    openai.api_key = openai_api_key

    prompt = f"""
Tu es un analyste financier. Voici les données pour {symbole} à {heure} :

Indicateurs :
{indicateurs}

Donne une recommandation claire de trading avec :
- Sens du trade (achat ou vente)
- Point d’entrée
- Stop loss
- Take profit
- Taux de probabilité de succès (en %)
- Un commentaire synthétique justifiant la recommandation
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
