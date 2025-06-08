from openai import OpenAI
from config import OPENAI_API_KEY
from datetime import datetime
import pytz

client = OpenAI(api_key=OPENAI_API_KEY)

def generer_signal_ia(symbole, heure, indicateurs):
    try:
        # Ajout du contexte horaire
        paris_tz = pytz.timezone("Europe/Paris")
        now = datetime.now(paris_tz)
        jour = now.strftime("%A")
        heure_locale = now.strftime("%H:%M")

        prompt = (
            f"Tu es un expert en trading algorithmique. Nous sommes {jour} et il est {heure_locale} à Paris.\n"
            f"Ton rôle est de générer un plan de trading clair et structuré.\n"
            f"Analyse les données suivantes pour {symbole} à {heure} :\n\n"
            f"{indicateurs}\n\n"
            f"Détermine :\n"
            f"1. La direction du trade : Long ou Short\n"
            f"2. Un niveau d'entrée (Entry)\n"
            f"3. Un stop loss\n"
            f"4. Trois take profits (TP1, TP2, TP3)\n"
            f"5. Le ratio minimum Risk/Reward sur TP1 doit être ≥ 1:1\n"
            f"6. Estime un taux de réussite entre 0% et 100%\n"
            f"7. Ne retourne un plan de trading que si le taux de réussite estimé est ≥ 70%\n\n"
            f"Réponds uniquement avec le plan de trading dans un format clair."
        )

        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en trading professionnel."},
                {"role": "user", "content": prompt}
            ]
        )
        return reponse.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur GPT pour {symbole} : {e}"
