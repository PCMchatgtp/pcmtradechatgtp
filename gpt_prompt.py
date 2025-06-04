from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generer_signal_ia(donnees, contexte_macro):
    prompt = f"""
Analyse les données suivantes et détermine s'il y a une opportunité de trade à court terme :
Actif : {donnees['actif']}
Prix actuel : {donnees['prix']}
Tendance : {donnees['tendance']}
MACD : {donnees['macd']}
Supports : {donnees['support']}
Résistances : {donnees['resistance']}
Contexte macroéconomique : {contexte_macro.get("résumé", "Non disponible")}

Donne uniquement une réponse si une opportunité de trade se présente. Sinon, dis 'Aucune opportunité'. Réponds en format JSON avec : direction, stop, tp1, tp2, tp3, justification.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un expert en trading à haute fréquence."},
            {"role": "user", "content": prompt}
        ]
    )

    contenu = response.choices[0].message.content.strip()
    return contenu
