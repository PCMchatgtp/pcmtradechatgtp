
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(symbole, tendance, heure, prix, volume, rsi, ema, macd):
    prompt = f'''
Tu es un expert en trading algorithmique. Voici les données de marché pour {symbole} :
- Heure : {heure}
- Prix : {prix}
- Volume : {volume}
- RSI : {rsi}
- EMA : {ema}
- MACD : {macd}
- Tendance : {tendance}

Analyse ces données et indique s’il y a une opportunité de trade. Donne un signal clair : Achat, Vente, ou Rien faire. Justifie ta réponse brièvement.
Ajoute une estimation du taux de réussite en pourcentage.

Réponse :
'''
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        return f"❌ Erreur GPT : {e}"
