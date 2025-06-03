from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generer_signal_ia(donnees, contexte_macro):
    try:
        if isinstance(contexte_macro, str):
            resume_macro = contexte_macro
        elif isinstance(contexte_macro, dict):
            resume_macro = contexte_macro.get("résumé", "Aucune donnée macro disponible.")
        else:
            resume_macro = "Format macro inconnu."

        prompt = f"""
Tu es un assistant de trading IA. Fournis un plan de trading pour {donnees['actif']} basé sur :
1. Les données de marché suivantes : prix actuel = {donnees['prix']}.
2. Le contexte macroéconomique : {resume_macro}.
3. Une analyse technique multi-timeframe (5min, 15min, 1h, 4h, daily, weekly).
Tu dois prévoir les zones de récupération de liquidité et anticiper les mouvements avec une stratégie à haut taux de réussite.

⚠️ Les conditions strictes sont :
- Entrée au marché immédiate
- Stop Loss obligatoire
- Take Profit 1 (TP1) avec un ratio de gain/risque minimum de 1:1 basé sur le TP1 (pas TP3)
- Break-even dès TP1 atteint
- Donne aussi TP2 et TP3 pour scalabilité

Retourne uniquement un objet JSON avec ces champs : actif, entrée, stop, tp1, tp2, tp3, break_even.
        """

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )

        contenu = completion.choices[0].message.content

        # Essaye d'évaluer le JSON
        import json
        signal = json.loads(contenu)
        return signal

    except Exception as e:
        raise ValueError(f"❌ Erreur GPT : {e}")
