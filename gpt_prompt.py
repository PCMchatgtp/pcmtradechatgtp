from openai import OpenAI
from config import OPENAI_API_KEY
from datetime import datetime
import pytz

client = OpenAI(api_key=OPENAI_API_KEY)

def generer_signal_ia(symbole, heure, indicateurs):
    try:
        paris_tz = pytz.timezone("Europe/Paris")
        now = datetime.now(paris_tz)
        jour = now.strftime("%A")
        heure_locale = now.strftime("%H:%M")

        prompt = (
            f"Tu es un expert en trading algorithmique.\n"
            f"Voici les données pour l’actif {symbole}, le {jour} à {heure_locale} (heure locale), "
            f"avec les données collectées à {heure} :\n\n"
            f"{indicateurs}\n\n"
            f"Tu dois privilégier la qualité, mais tu peux proposer un plan si plusieurs éléments convergents sont identifiables "
            f(même si tout n’est pas parfaitement aligné).\n"
            f"Ne propose un plan que si on observe un minimum de cohérence entre la structure, les niveaux clés et la dynamique du marché.\n"
            f"Si aucune lecture exploitable n’est possible, réponds UNIQUEMENT : 'Aucune opportunité claire détectée.'\n\n"
            f"Sinon, donne :\n"
            f"1. Direction (Long ou Short)\n"
            f"2. Niveau d’entrée\n"
            f"3. Niveau de stop\n"
            f"4. TP1, TP2, TP3\n"
            f"5. Risk/Reward sur TP1 (minimum 1:1 requis)\n"
            f"6. Taux de réussite estimé (entre 0 % et 100 %)\n\n"
            f"N'affiche le plan que si le taux est ≥ 50 %.\n"
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

# 🔍 Fonction spéciale pour la stratégie OPR
def generer_signal_opr(symbole, heure, indicateurs, high_range, low_range):
    try:
        paris_tz = pytz.timezone("Europe/Paris")
        now = datetime.now(paris_tz)
        heure_locale = now.strftime("%H:%M")

        prompt = (
            f"Tu es un expert en stratégie OPR (Opening Price Range) sur le marché du {symbole}.\n"
            f"Il est actuellement {heure_locale}, heure locale de Paris. Voici les données analysées :\n\n"
            f"{indicateurs}\n\n"
            f"Le range initial 15h30–15h45 (heure de Paris) est défini comme suit :\n"
            f"- Plus haut : {high_range}\n"
            f"- Plus bas : {low_range}\n\n"
            f"Tu dois observer si une cassure claire s’est produite AU-DESSUS ou EN-DESSOUS de ce range "
            f"dans les minutes qui suivent (jusqu’à 16h15).\n"
            f"Si oui, propose un plan de trade cohérent avec la cassure détectée.\n"
            f"Sinon, réponds uniquement : 'Pas de cassure, aucune prise de position OPR à envisager.'\n\n"
            f"Si cassure, donne :\n"
            f"1. Direction (Long ou Short selon la cassure)\n"
            f"2. Niveau d’entrée\n"
            f"3. Stop\n"
            f"4. TP1, TP2, TP3\n"
            f"5. Risk/Reward sur TP1 (≥ 1:1)\n"
            f"6. Taux de réussite estimé\n"
            f"Uniquement si le taux est ≥ 50 %, le plan est accepté."
        )

        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en stratégie OPR sur les marchés financiers."},
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(reponse, "choices") and len(reponse.choices) > 0:
            return reponse.choices[0].message.content
        else:
            return f"❌ Erreur : réponse vide ou inattendue de GPT pour stratégie OPR sur {symbole}"

    except Exception as e:
        return f"❌ Erreur GPT OPR pour {symbole} : {e}"
