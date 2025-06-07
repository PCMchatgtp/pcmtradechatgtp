import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(symbole, heure, indicateurs):
    prompt = f"""
Tu es un expert du marché. Donne une analyse synthétique sur {symbole}.
Voici les indicateurs disponibles :
- Heure actuelle : {heure}
- Open : {indicateurs.get("open")}
- High : {indicateurs.get("high")}
- Low : {indicateurs.get("low")}
- Close : {indicateurs.get("close")}
- Volume : {indicateurs.get("volume")}

Dis-moi :
1. Si une opportunité de trading est présente.
2. Quel type de position (achat ou vente).
3. Donne une entrée, un stop, et un TP1 (le ratio R:R > 1 obligatoire).
4. Ajoute un pourcentage de confiance.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response["choices"][0]["message"]["content"]