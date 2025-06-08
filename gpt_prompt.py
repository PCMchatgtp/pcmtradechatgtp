from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generer_signal_ia(symbole, tendance, heure, indicateurs):
    prompt = f"""
Analyse technique IA pour {symbole}
Tendance actuelle : {tendance}
Heure : {heure}
Indicateurs disponibles :
{indicateurs}

Fournis une suggestion de trade avec : point d'entrée, stop loss, TP1, TP2, TP3. Ajoute un commentaire stratégique.
"""
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse de marché."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur IA : {e}"