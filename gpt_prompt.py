from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generer_signal_ia(symbole, donnees, heure, indicateurs):
    prompt = f"""Tu es un expert en trading. Voici les données de marché pour {symbole} à {heure} :

Données (5 dernières bougies) :
{donnees[:5]}

Indicateurs :
{indicateurs}

Donne un plan de trading clair et concis :
- Achat ou vente ?
- Entrée, stop loss, TP1, TP2, TP3
- Justification basée sur les données ci-dessus
- Ne donne un plan que si une opportunité réelle est présente
"""

    reponse = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=800
    )

    return reponse.choices[0].message.content.strip()