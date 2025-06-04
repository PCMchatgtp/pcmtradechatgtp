from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generer_signal_ia(donnees, tendance, heure, contexte_macro):
    message = f"""
    Actif : {donnees['actif']}
    Prix actuel : {donnees['prix']}
    Heure : {heure}
    Tendance : {tendance}
    Contexte macro : {contexte_macro}
    Analyse les données précédentes et indique si une opportunité de trade existe. 
    Si oui, donne le sens (achat ou vente), le point d’entrée, le stop et les TP.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content
