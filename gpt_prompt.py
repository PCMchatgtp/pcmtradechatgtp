import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generer_signal_ia(donnees, contexte):
    actif = donnees["actif"]
    symbol = donnees["symbol"]
    timeframes = donnees["timeframes"]

    prompt = f"""
Tu es une IA de trading spécialisée prop firm.

Actif : {actif} ({symbol})
Contexte multi-timeframe : 5m, 15m, 1h, 4h, 1d, 1w
Contexte macroéconomique :
{contexte}

Ta mission :
1. Analyse les bougies.
2. Évalue le contexte macro + fondamental.
3. Si opportunité claire → propose un plan.

⚠️ Critère obligatoire :
- (TP1 - Entrée) / (Entrée - SL) ≥ 1
- Sinon : "Pas d'entrée pertinente actuellement."

Format unique si opportunité :

🎯 Plan pour {actif} :

- Action : [Acheter/Vendre]
- Entrée : [niveau]
- Stop Loss : [niveau]
- TP1 : [niveau]
- TP2 : [niveau]
- TP3 : [niveau]
- Break-even : [niveau ou condition]
- Taux de confiance : [XX %]
- Justification : [2 phrases max]
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()
