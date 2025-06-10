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
            f"Tu es un expert en trading algorithmique.\n"
            f"Voici les données pour l’actif {symbole}, le {jour} à {heure_locale} (heure locale), "
            f"avec les données collectées à {heure} :\n\n"
            f"Tu dois privilégier la qualité, mais accepter les opportunités raisonnablement claires :\n"
            f"Ne propose un plan que si les indicateurs sont suffisamment alignés (structure + cassure ou support + flux propre).\n"
            f"NE FOURNIS AUCUN PLAN si les indicateurs ne sont pas parfaitement alignés "
            f"(ex : pas de cassure, structure peu claire, volume faible).\n\n"
            f"Si les conditions ne sont pas claires, réponds UNIQUEMENT : 'Aucune opportunité claire détectée.'\n\n"
            f"Sinon, si tout est parfaitement aligné, donne :\n"
            f"1. Direction (Long ou Short)\n"
            f"2. Niveau d’entrée\n"
            f"3. Niveau de stop\n"
            f"4. TP1, TP2, TP3\n"
            f"5. Risk/Reward sur TP1 (minimum 1:1 requis)\n"
            f"6. Taux de réussite estimé (entre 0 % et 100 %)\n\n"
            f"N'affiche le plan que si le taux est ≥ 60 %.\n"
        )

        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en trading professionnel."},
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(reponse, "choices") and len(reponse.choices) > 0:
            return reponse.choices[0].message.content
        else:
            return f"❌ Erreur : réponse vide ou inattendue de GPT pour {symbole}"

    except Exception as e:
        return f"❌ Erreur GPT pour {symbole} : {e}"
