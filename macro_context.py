import os
import requests
from datetime import datetime, timedelta

FMP_API_KEY = os.getenv("FMP_API_KEY")
SHEET_URL = os.getenv("GOOGLE_SHEET_WEBHOOK")

def envoyer_vers_google_sheet(event):
    try:
        payload = {
            "country": event.get("country", "N/A"),
            "hour": event.get("date", "N/A"),
            "event": event.get("event", "N/A"),
            "importance": event.get("impact", "N/A"),
            "actual": event.get("actual", "N/A"),
            "forecast": event.get("forecast", "N/A"),
            "previous": event.get("previous", "N/A")
        }
        requests.post(SHEET_URL, json=payload)
    except Exception as e:
        print(f"Erreur envoi vers Google Sheet : {e}")

def contexte_macro_simplifie():
    try:
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        url = f"https://financialmodelingprep.com/api/v3/economic_calendar?from={today}&to={tomorrow}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        events = response.json()

        lignes = []
        for e in events:
            if e.get("impact") in ["High", "Medium"]:
                envoyer_vers_google_sheet(e)
                ligne = f"• {e.get('country', 'N/A')} - {e.get('date', 'N/A')} : {e.get('event', 'N/A')} ({e.get('impact', 'N/A')}) → Act: {e.get('actual', 'n/a')} / Prév: {e.get('forecast', 'n/a')} / Anc: {e.get('previous', 'n/a')}"
                lignes.append(ligne)

        if lignes:
            return "📅 Événements macroéconomiques importants du jour :\n" + "\n".join(lignes[:10])
        else:
            return "📅 Aucun événement économique majeur prévu aujourd’hui dans les zones concernées."

    except Exception as e:
        return f"❌ Erreur macro API : {e}"
