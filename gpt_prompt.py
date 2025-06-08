from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generer_signal_ia(symbole, heure, indicateurs):
    try:
        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en trading."},
                {"role": "user", "content": f"Donne une analyse pour {symbole} à {heure} avec ces données : {indicateurs}"}
            ]
        )
        return reponse.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur GPT pour {symbole} : {e}"