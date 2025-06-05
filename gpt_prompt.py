import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(donnees):
    prompt = f"""
Analyse ce marché : {donnees['symbole']}, avec un prix actuel de {donnees['prix']}.
Tu es un expert en scalping à court terme. Indique s’il y a une opportunité de trade.

Règles :
- Analyse uniquement si le marché est propice.
- Propose un trade clair (achat ou vente) seulement si le TP1 respecte un ratio gain/risque > 1.
- Si aucune opportunité valable n’est détectée, retourne vide.
- Donne un plan avec entrée, stop, TP1, TP2, TP3, un pourcentage de réussite estimé et un commentaire concis.

Réponds uniquement si un trade est pertinent.
"""

    try:
        reponse = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        message = reponse["choices"][0]["message"]["content"]
        return message if "entrée" in message and "stop" in message and "TP1" in message else ""
    except Exception as e:
        return f"❌ Erreur GPT : {e}"