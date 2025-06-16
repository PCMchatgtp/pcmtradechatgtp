from openai import OpenAI
from config import OPENAI_API_KEY
from datetime import datetime
import pytz
import re

client = OpenAI(api_key=OPENAI_API_KEY)

def enrichir_indicateurs(indicateurs_bruts):
    resume = []

    # RSI
    rsi_match = re.search(r"RSI\s*\(14\)\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts, re.IGNORECASE)
    if rsi_match:
        rsi = float(rsi_match.group(1))
        if rsi > 70:
            resume.append(f"RSI {rsi} (surachat)")
        elif rsi < 30:
            resume.append(f"RSI {rsi} (survente)")
        else:
            resume.append(f"RSI {rsi} (neutre)")
    else:
        resume.append("RSI non détecté")

    # MACD
    macd_match = re.search(r"MACD\s*[:\-]?\s*([\d\.\-]+)", indicateurs_bruts, re.IGNORECASE)
    signal_match = re.search(r"Signal\s*[:\-]?\s*([\d\.\-]+)", indicateurs_bruts, re.IGNORECASE)
    if macd_match and signal_match:
        macd = float(macd_match.group(1))
        signal = float(signal_match.group(1))
        direction_macd = "MACD haussier" if macd > signal else "MACD baissier" if macd < signal else "MACD neutre"
        resume.append(f"{direction_macd} ({macd} vs {signal})")
    else:
        resume.append("MACD non détecté")

    # VWAP
    vwap_match = re.search(r"VWAP\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts, re.IGNORECASE)
    close_match = re.search(r"Prix clôture\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts)
    if vwap_match and close_match:
        vwap = float(vwap_match.group(1))
        close = float(close_match.group(1))
        if close > vwap:
            resume.append(f"Prix au-dessus du VWAP ({close} > {vwap})")
        else:
            resume.append(f"Prix sous le VWAP ({close} < {vwap})")
    else:
        resume.append("VWAP non détecté")

    # Tendance
    tendance_match = re.search(r"Tendance\s*[:\-]?\s*(\w+)", indicateurs_bruts, re.IGNORECASE)
    if tendance_match:
        resume.append(f"Tendance globale : {tendance_match.group(1).capitalize()}")
    else:
        resume.append("Tendance non détectée")

    # Bollinger Bands
    boll_upper = re.search(r"Bollinger Haut\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts, re.IGNORECASE)
    boll_lower = re.search(r"Bollinger Bas\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts, re.IGNORECASE)
    if boll_upper and boll_lower and close_match:
        upper = float(boll_upper.group(1))
        lower = float(boll_lower.group(1))
        close = float(close_match.group(1))
        if close > upper:
            resume.append(f"Clôture au-dessus des bandes de Bollinger")
        elif close < lower:
            resume.append(f"Clôture sous les bandes de Bollinger")
        else:
            resume.append(f"Clôture à l'intérieur des bandes de Bollinger")
    else:
        resume.append("Bollinger non détecté")

    # Range & taille de bougie
    range_match = re.search(r"Range\s*\(H\-L\)\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts)
    body_match = re.search(r"Taille corps\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts)
    if range_match and body_match:
        resume.append(f"Range : {range_match.group(1)} | Corps : {body_match.group(1)}")

    # Variation %
    variation = re.search(r"Variation %\s*[:\-]?\s*([\d\.\-]+)%", indicateurs_bruts)
    if variation:
        resume.append(f"Variation sur la bougie : {variation.group(1)}%")

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
            f"Propose un plan même si les données sont imparfaites. Structure ta réponse ainsi :\n"
            f"1. Direction (Long ou Short)\n"
            f"2. Niveau d’entrée\n"
            f"3. Stop loss\n"
            f"4. TP1, TP2, TP3\n"
            f"5. Risk/Reward sur TP1 (≥ 1:1)\n"
            f"6. Taux de réussite estimé (0 à 100 %)\n"
            f"Ne génère rien si aucune configuration pertinente ne se dégage."
        )

        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en trading professionnel."},
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(reponse, "choices") and len(reponse.choices) > 0:
            contenu = reponse.choices[0].message.content.strip()
            if any(x in contenu.lower() for x in ["aucune opportunité", "pas de plan", "difficile de dire"]):
                return ""  # Ne rien renvoyer pour Telegram
            return contenu
        else:
            return ""

    except Exception as e:
        return f"❌ Erreur GPT pour {symbole} : {e}"

def generer_signal_opr(symbole, heure, indicateurs, high_range, low_range):
    try:
        paris_tz = pytz.timezone("Europe/Paris")
        now = datetime.now(paris_tz)
        heure_locale = now.strftime("%H:%M")

        prompt = (
            f"Tu es un expert en stratégie OPR (Opening Price Range) sur le marché du {symbole}.\n"
            f"Il est actuellement {heure_locale}, heure de Paris. Voici les données :\n\n"
            f"{indicateurs}\n\n"
            f"Le range 15h30–15h45 est :\n"
            f"- Plus haut : {high_range}\n"
            f"- Plus bas : {low_range}\n\n"
            f"Tu dois détecter toute cassure de ce range.\n"
            f"Propose un plan si la cassure est claire. Ne réponds pas si aucune cassure.\n\n"
            f"Structure :\n"
            f"1. Direction\n2. Entrée\n3. Stop\n4. TP1, TP2, TP3\n5. R/R TP1\n6. Taux de réussite estimé"
        )

        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en stratégie OPR sur les marchés financiers."},
                {"role": "user", "content": prompt}
            ]
        )

        if hasattr(reponse, "choices") and len(reponse.choices) > 0:
            contenu = reponse.choices[0].message.content.strip()
            if "aucune cassure" in contenu.lower() or "pas de cassure" in contenu.lower():
                return ""
            return contenu
        else:
            return ""

    except Exception as e:
        return f"❌ Erreur GPT OPR pour {symbole} : {e}"
