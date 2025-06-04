import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generer_signal_ia(donnees, contexte_macro):
    prompt = f'''
Tu es un expert en scalping court terme. Voici les données de marché :

Actif : {donnees['actif']}
Prix actuel : {donnees['prix']}
Contexte macro : {contexte_macro}

Analyse la situation. Si une opportunité se présente, fournis un plan clair.
Sinon, indique qu'il n'y a pas d'opportunité.

Format de réponse JSON :
{{
  "actif": "...",
  "prix": ...,
  "tendance": "...",
  "heure": "...",
  "contexte_macro": "...",
  "opportunite": true/false,
  "plan": {{
    "entree": ...,
    "stop": ...,
    "tp1": ...,
    "tp2": ...,
    "tp3": ...
  }}
}}
'''
    reponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    message = reponse["choices"][0]["message"]["content"]
    return message