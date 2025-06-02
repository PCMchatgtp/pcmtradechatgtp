import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("TOKEN =", TOKEN)
print("CHAT_ID =", CHAT_ID)

if not TOKEN or not CHAT_ID:
    raise ValueError("❌ TOKEN ou CHAT_ID manquant dans Render.")
