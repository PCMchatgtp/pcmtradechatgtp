from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generer_signal_ia(symbole, tendance, heure, indicateurs):
    prompt = f"""
    Tu es un analyste financier professionnel. Tu dois générer une analyse de marché sur l'actif {symbole} basé sur :

    - la tendance actuelle : {tendance}
    - l’heure de l’analyse : {heure}
    - les indicateurs techniques suivants : {indicateurs}

    Génère une stratégie claire avec :
    - un point d’entrée
    - un stop loss
    - un ou plusieurs take profits
    - un pourcentage de probabilité de réussite
    - un court commentaire stratégique justifiant le plan proposé

    Format clair et structuré.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un expert en trading algorithmique."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
