def generer_signal_ia(donnees, contexte_macro):
    actif = donnees["actif"]
    prix = donnees["prix"]
    
    # Exemple très simple d’IA logique. À affiner.
    decision = "attendre"
    if actif == "XAUUSD" and float(prix) < 2400:
        decision = "prendre position"
    elif actif == "NASDAQ" and float(prix) > 17000:
        decision = "prendre position"

    return {
        "macro": contexte_macro.get("résumé", "Données macro indisponibles") if isinstance(contexte_macro, dict) else contexte_macro,
        "entree": prix,
        "stop": round(float(prix) - 15, 2),
        "tp1": round(float(prix) + 30, 2),
        "tp2": round(float(prix) + 60, 2),
        "tp3": round(float(prix) + 90, 2),
        "decision": decision,
    }
