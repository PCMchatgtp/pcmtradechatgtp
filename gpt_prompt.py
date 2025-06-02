def generer_signal_ia(donnees, contexte_macro):
    try:
        actif = donnees["actif"]
        prix = donnees["prix"]

        stop = round(prix - 17, 2)
        tp1 = round(prix + 33, 2)
        tp2 = round(prix + 67, 2)
        tp3 = round(prix + 101, 2)

        rr = (tp1 - prix) / (prix - stop)
        if rr < 1.0:
            raise ValueError("❌ R:R < 1:1 — plan ignoré")

        return {
            "entree": prix,
            "stop": stop,
            "tp1": tp1,
            "tp2": tp2,
            "tp3": tp3,
            "macro": contexte_macro  # 🟢 Contexte texte simple, plus de .get()
        }

    except Exception as e:
        raise ValueError(f"❌ Erreur dans l’analyse IA : {e}")
