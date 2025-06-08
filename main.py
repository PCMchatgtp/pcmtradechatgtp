async def main():
    bot = Bot(token=TOKEN)
    fuseau = pytz.timezone('Europe/Paris')
    maintenant = datetime.now(fuseau)
    heure = maintenant.strftime('%H:%M')

    resume = f"🕒 **Résumé de l’analyse à {heure}**\n"
    for actif, (heure_debut, heure_fin) in SYMBOLS.items():
        try:
            if not heure_debut <= maintenant.hour < heure_fin:
                continue

            print(f"Analyse de {actif}...")

            symbol = actif
            nom_affichage = actif.replace("_", "/")
            donnees, indicateurs = recuperer_donnees(symbol, twelve_data_api_key)
            if donnees is None or indicateurs is None:
                raise ValueError("❌ Erreur lors de l'extraction des données.")

            plan, commentaire = generer_signal_ia(symbol, heure, indicateurs)

            message = f"💡 *Signal IA pour {nom_affichage}* à {heure}:\n\n{plan}\n\n🧠 _{commentaire}_"
            await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
            resume += f"✅ {nom_affichage} : OK\n"

        except Exception as e:
            resume += f"❌ {actif.replace('_', '/')} : Erreur – {str(e).splitlines()[0][:60]}\n"

    await bot.send_message(chat_id=CHAT_ID, text=resume)
