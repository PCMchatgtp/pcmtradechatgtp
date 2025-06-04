def generer_signal_ia(donnees):
    actif = donnees["actif"]
    prix = donnees["prix"]
    tendance = donnees["tendance"]
    heure = donnees["heure"]

    if actif == "XAUUSD" and not (7 <= heure.hour <= 22):
        return None

    if actif == "NASDAQ" and not (15 <= heure.hour <= 18):
        return None

    if tendance != "hausse":
        return None

    tp1 = round(prix * 1.01, 2)
    tp2 = round(prix * 1.02, 2)
    tp3 = round(prix * 1.03, 2)
    sl = round(prix * 0.99, 2)

    return f"""📡 Signal pour {actif} :

📊 Analyse IA
Actif : {actif}
Prix actuel : {prix}
Tendance détectée : {tendance}

🔁 Entrée : {prix}
📉 Stop : {sl}
📈 TP1 : {tp1}
📈 TP2 : {tp2}
📈 TP3 : {tp3}
🎯 Break-even après TP1 atteint.""" 
