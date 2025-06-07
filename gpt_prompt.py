import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generer_signal_ia(symbole, cours, heure, indicateurs):
    prompt = f'''
Analyse IA pour {symbole}
Heure : {heure}
Prix actuel : {cours['close']}
Volume : {cours['volume']}
Historique cours : {indicateurs['close'][:5]}
Historique volume : {indicateurs['volume'][:5]}

Donne un plan de trading simple (entrée, stop, TP1, TP2, TP3) avec un commentaire de stratégie.
'''
    reponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return reponse["choices"][0]["message"]["content"]