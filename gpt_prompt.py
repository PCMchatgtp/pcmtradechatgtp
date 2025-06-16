from openai import OpenAI
from config import OPENAI_API_KEY
from datetime import datetime
import pytz

client = OpenAI(api_key=OPENAI_API_KEY)

def generer_signal_ia(symbole, heure, indicateurs_bruts):
    try:
        paris_tz = pytz.timezone("Europe/Paris")
        now = datetime.now(paris_tz)
        jour = now.strftime("%A")
        heure_locale = now.strftime("%H:%M")

        prompt = (
            f"Tu es un expert en trading algorithmique.\n"
            f"Voici l’analyse technique actuelle de {symbole}, le {jour} à {heure_locale} :\n\n"
            f"{indicateurs_bruts}\n\n"
            f"Tu dois toujours proposer un plan clair même si les données sont partielles ou contradictoires.\n"
            f"N'invente rien, mais déduis logiquement une direction si possible. Tu peux aussi indiquer un biais neutre.\n\n"
            f"Donne un plan structuré comme ceci :\n"
            f"1. Direction (Long, Short ou Neutre)\n"
            f"2. Niveau d’entrée\n"
            f"3. Stop loss\n"
            f"4. TP1, TP2, TP3\n"
            f"5. Risk/Reward sur TP1 (au moins 1:1)\n"
            f"6. Taux de réussite estimé (0 à 100 %)\n"
        )

        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en stratégie de trading professionnel à haut rendement."},
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(reponse, "choices") and len(reponse.choices) > 0:
            return reponse.choices[0].message.content
        else:
            return f"❌ Erreur : réponse vide ou inattendue de GPT pour {symbole}"

    except Exception as e:
        return f"❌ Erreur GPT pour {symbole} : {e}"


def generer_signal_opr(symbole, heure, indicateurs, high_range, low_range):
    try:
        paris_tz = pytz.timezone("Europe/Paris")
        now = datetime.now(paris_tz)
        heure_locale = now.strftime("%H:%M")

        prompt = (
            f"Tu es un expert en stratégie OPR (Opening Price Range) sur le marché du {symbole}.\n"
            f"Il est actuellement {heure_locale}, heure de Paris. Voici les indicateurs actuels :\n\n"
            f"{indicateurs}\n\n"
            f"Le range initial de 15h30 à 15h45 (heure Paris) est défini comme :\n"
            f"- Plus haut : {high_range}\n"
            f"- Plus bas : {low_range}\n\n"
            f"Analyse les cassures potentielles (haussière ou baissière), même si les données sont partielles.\n"
            f"Ne refuse jamais de répondre. Construis une stratégie plausible si une cassure est visible.\n\n"
            f"Plan à donner :\n"
            f"1. Direction (Long ou Short)\n"
            f"2. Niveau d’entrée\n"
            f"3. Stop loss\n"
            f"4. TP1, TP2, TP3\n"
            f"5. Risk/Reward sur TP1 (≥ 1:1)\n"
            f"6. Taux de réussite estimé"
        )

        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en stratégie OPR sur les marchés financiers."},
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(reponse, "choices") and len(reponse.choices) > 0:
            return reponse.choices[0].message.content
        else:
            return f"❌ Erreur : réponse vide ou inattendue de GPT pour stratégie OPR sur {symbole}"

    except Exception as e:
        return f"❌ Erreur GPT OPR pour {symbole} : {e}"
