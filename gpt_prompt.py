from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generer_signal_ia(symbole, tendance, heure, indicateurs):
    prompt = f"""
Analyse IA pour {symbole} à {heure}
Tendance : {tendance}
Indicateurs : {indicateurs}

En te basant sur ces éléments, génère une stratégie de trading : direction, point d’entrée, stop loss, TP1, TP2, TP3.
Donne aussi un commentaire expliquant la logique et une estimation de taux de réussite.
"""
    reponse = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return reponse.choices[0].message.content
