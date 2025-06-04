import openai
import os

# Chargement de la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def generer_signal_ia(donnees, tendance, heure, contexte_macro):
    """
    Génère une analyse de signal de trading à partir des données de marché,
    de la tendance, de l'heure actuelle et du contexte macroéconomique.
    """
    prompt = f"""
Tu es un assistant de trading expert qui travaille en scalping sur des unités de temps très courtes (ex: 5 minutes).

Ton objectif est de détecter UNIQUEMENT les opportunités de trade à forte probabilité, et de NE RIEN ENVOYER s'il n'y a pas de configuration évidente ou exploitable.

Tu bases ton raisonnement sur les données suivantes :
- Actif : {donnees['actif']}
- Prix actuel : {donnees['prix']}
- Variation récente : {donnees['variation']}%
- Heure actuelle : {heure}
- Tendance technique détectée : {tendance}
- Contexte macro-économique : {contexte_macro}

Règles impératives :
- Pas de trade si les conditions ne sont pas claires.
- Uniquement des trades intraday (scalping) avec sortie dans la journée.
- Interdis les niveaux irréalistes (exemple : BTC à 105000 si le prix est à 70000).
- Propose soit un achat (long), soit une vente (short), jamais les deux à la fois.
- Ne propose PAS de trade si les conditions sont neutres ou trop incertaines.

Format de réponse attendu :
Analyse :
<ton analyse en 2 phrases max>

Sens du trade :
<"Achat" ou "Vente" ou "Aucune opportunité">

Entrée :
<prix d’entrée>

Stop :
<stop loss>

TP1 :
<take profit 1>

TP2 :
<take profit 2 (optionnel)>

TP3 :
<take profit 3 (optionnel)>

Remarque : Sois précis, ne répète pas d’évidences. Tu t’adresses à un trader confirmé.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Tu peux utiliser gpt-4 si ton plan le permet
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Erreur GPT : {e}"
