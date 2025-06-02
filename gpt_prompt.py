import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(actif, donnees_techniques, contexte_macro):
    prompt = f"""
Tu es un analyste financier expérimenté. Analyse l'actif {actif} avec les données suivantes :
Analyse technique :
{donnees_techniques}

Contexte macroéconomique actuel :
{contexte_macro}

Dis s’il y a une opportunité de trade claire. Si oui, donne :
- Tendance (haussière, baissière)
- Point d’entrée conseillé
- Stop loss
- Take profit
- Confiance (%)
- Logique de décision
Sinon, dis "Pas de signal exploitable pour l’instant."
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']
