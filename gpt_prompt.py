from openai import OpenAI
from config import OPENAI_API_KEY
from datetime import datetime
import pytz
import re

client = OpenAI(api_key=OPENAI_API_KEY)

def enrichir_indicateurs(indicateurs_bruts):
    resume = []

    rsi_match = re.search(r"RSI\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts, re.IGNORECASE)
    if rsi_match:
        rsi = float(rsi_match.group(1))
        if rsi > 70:
            resume.append(f"RSI {rsi} (surachat)")
        elif rsi < 30:
            resume.append(f"RSI {rsi} (survente)")
        else:
            resume.append(f"RSI {rsi} (zone neutre)")
    else:
        resume.append("RSI non détecté")

    macd_match = re.search(r"MACD\s*[:\-]?\s*([\d\.\-]+)", indicateurs_bruts, re.IGNORECASE)
    signal_match = re.search(r"Signal\s*[:\-]?\s*([\d\.\-]+)", indicateurs_bruts, re.IGNORECASE)
    if macd_match and signal_match:
        macd = float(macd_match.group(1))
        signal = float(signal_match.group(1))
        if macd > signal:
            resume.append(f"MACD haussier ({macd} > {signal})")
        elif macd < signal:
            resume.append(f"MACD baissier ({macd} < {signal})")
        else:
            resume.append("MACD neutre")
    else:
        resume.append("MACD non détecté")

    volume_match = re.search(r"Volume\s*[:\-]?\s*([\d\.kKmM]+)", indicateurs_bruts, re.IGNORECASE)
    if volume_match:
        resume.append(f"Volume : {volume_match.group(1)}")
    else:
        resume.append("Volume non détecté")

    ma_matches = re.findall(r"(EMA|SMA)[\s\-]?\d+\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts, re.IGNORECASE)
    if ma_matches:
        resume.extend([f"{ma[0].upper()} : {ma[1]}" for ma in ma_matches])
    else:
        resume.append("Pas de moyenne mobile détectée")

    return "\n".join(resume)

def generer_signal_ia(symbole, heure, indicateurs_bruts):
    try:
        paris_tz = pytz.timezone("Europe/Paris")
        now = datetime.now(paris_tz)
        jour = now.strftime("%A")
        heure_locale = now.strftime("%H:%M")
        indicateurs = enrichir_indicateurs(indicateurs_bruts)

        prompt = (
            f"Tu es un expert en trading algorithmique.\n"
            f"Voici l’analyse technique actuelle de {symbole}, le {jour} à {heure_locale} :\n\n"
            f"{indicateurs}\n\n"
            f"Tu dois toujours proposer un plan, même si les données sont imparfaites ou contradictoires.\n"
            f"Fais de ton mieux avec ce que tu as. Propose un plan même risqué ou incertain si un mouvement est plausible.\n\n"
            f"Donne un plan structuré :\n"
            f"1. Direction (Long ou Short)\n"
            f"2. Niveau d’entrée\n"
            f"3. Stop loss\n"
            f"4. TP1, TP2, TP3\n"
            f"5. Risk/Reward sur TP1 (≥ 1:1)\n"
            f"6. Taux de réussite estimé (0 à 100 %)"
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
            f"Tu dois détecter toute cassure au-dessus ou en dessous de ce range.\n"
            f"Si une cassure est visible, propose un plan même si les conditions sont imparfaites.\n"
            f"Ne refuse jamais de répondre. Utilise ton expérience pour construire une stratégie exploitable.\n\n"
            f"Plan à donner :\n"
            f"1. Direction (Long ou Short)\n"
            f"2. Niveau d’entrée\n"
            f"3. Stop\n"
            f"4. TP1, TP2, TP3\n"
            f"5. Risk/Reward sur TP1 (≥ 1:1)\n"
            f"6. Taux de réussite estimé"
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
