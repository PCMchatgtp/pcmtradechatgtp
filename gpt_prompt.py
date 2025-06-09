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
    f"Tu es un expert en trading algorithmique. Tu dois ABSOLUMENT filtrer les opportunités :\n"
    f"NE FOURNIS AUCUN PLAN si les indicateurs ne sont pas parfaitement alignés.\n"
    f"Tu dois être extrêmement exigeant et prudent.\n"
    f"Voici les données pour {symbole} à {heure} :\n\n"
    f"{indicateurs}\n\n"
    f"Si les conditions ne sont pas claires (ex : pas de cassure, pas de structure propre, volume faible), réponds uniquement : 'Aucune opportunité claire détectée.'\n"
    f"Sinon, si tout est parfaitement aligné, donne :\n"
    f"1. Direction (Long ou Short)\n"
    f"2. Entrée\n"
    f"3. Stop\n"
    f"4. TP1, TP2, TP3\n"
    f"5. Risk/Reward sur TP1 (obligatoire ≥ 1:1)\n"
    f"6. Taux de réussite estimé entre 0 % et 100 %\n"
    f"Uniquement si le taux est ≥ 70 %, le plan est accepté.\n"
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
