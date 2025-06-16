def enrichir_indicateurs(indicateurs_bruts):
    resume = []

    lignes = indicateurs_bruts.strip().splitlines()
    for ligne in lignes:
        if ":" in ligne:
            resume.append(ligne.strip())

    # RSI interprété
    rsi_match = re.search(r"RSI\s*\(14\)\s*[:\-]?\s*([\d\.]+)", indicateurs_bruts, re.IGNORECASE)
    if rsi_match:
        rsi = float(rsi_match.group(1))
        if rsi > 70:
            resume.append(f"📈 RSI {rsi} → Surachat")
        elif rsi < 30:
            resume.append(f"📉 RSI {rsi} → Survente")
        else:
            resume.append(f"🔄 RSI {rsi} → Zone neutre")
    else:
        resume.append("⚠️ RSI non détecté")

    # Tendance détectée
    tendance_match = re.search(r"Tendance\s*[:\-]?\s*(\w+)", indicateurs_bruts, re.IGNORECASE)
    if tendance_match:
        resume.append(f"📊 Tendance : {tendance_match.group(1).capitalize()}")

    # Variation %
    var_match = re.search(r"Variation\s*%\s*[:\-]?\s*([-+]?\d+\.?\d*)", indicateurs_bruts)
    if var_match:
        variation = float(var_match.group(1))
        direction = "hausse" if variation > 0 else "baisse" if variation < 0 else "stable"
        resume.append(f"📉 Variation sur 5min : {variation:.2f}% ({direction})")

    return "\n".join(resume)
