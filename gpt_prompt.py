from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generer_signal_ia(symbole, heure, indicateurs):
    try:
        prompt = f"""
Tu es un expert en trading algorithmique. Voici les indicateurs techniques pour {symbole} à {heure} :

- Open : {indicateurs.get('open', 'N/A')}
- High : {indicateurs.get('high', 'N/A')}
- Low : {indicateurs.get('low', 'N/A')}
- Close : {indicateurs.get('close', 'N/A')}
- Volume : {indicateurs.get('volume', 'N/A')}
- Datetime : {indicateurs.get('datetime', 'N/A')}
- Average Price : {indicateurs.get('average_price', 'N/A')}
- Range (High - Low) : {indicateurs.get('range', 'N/A')}
- Body Size (|Close - Open|) : {indicateurs.get('body_size', 'N/A')}
- Upper Wick : {indicateurs.get('upper_wick', 'N/A')}
- Lower Wick : {indicateurs.get('lower_wick', 'N/A')}
- Pourcentage de variation : {indicateurs.get('percentage_change', 'N/A')}%
- Bougie haussière : {indicateurs.get('bullish', 'N/A')}

Analyse la situation et indique :
1. S'il existe une opportunité de trade (achat ou vente),
2. Pourquoi (justifie avec les indicateurs),
3. Sinon, pourquoi s’abstenir.

Ne commente pas les données absentes. Sois clair, synthétique et orienté décision.
"""
        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en trading."},
                {"role": "user", "content": prompt}
            ]
        )
        return reponse.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur GPT pour {symbole} : {e}"
