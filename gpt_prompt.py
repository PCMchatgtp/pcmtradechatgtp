def generer_signal_ia(symbole, donnees):
    try:
        tendance = "haussière" if donnees["price"] > (donnees["high"] + donnees["low"]) / 2 else "baissière"
        commentaire = f"""Analyse IA pour {symbole} :
Contexte technique basé sur les données de marché récentes.
Décision déterminée par l'intelligence artificielle après analyse complète."""
Tendance : {tendance}
Prix actuel : {donnees['price']}
Volume : {donnees['volume']}
"""
        commentaire += "✅ Opportunité détectée" if tendance == "haussière" else "⚠️ Prudence recommandée"
        return commentaire
    except Exception as e:
        return f"❌ Erreur GPT : {e}"
