from config import OPENAI_API_KEY
import openai

def generer_signal_ia(symbole, donnees, heure, indicateurs):
    prompt = f"""
Analyse les données suivantes pour {symbole} à {heure}.
Cours : {donnees}
Indicateurs : {indicateurs}
Donne un signal de trading avec justification (achat, vente ou neutre).
"""
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()