from flask import Flask, jsonify
import os
import threading
import sys
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent, DisconnectEvent

# ✅ WHITELIST — adiciona os nicks do TikTok aqui
WHITELIST = [
    "@weverti04",
    # "@nick_do_comprador1",
]

# pega o nick do terminal ou usa o primeiro da whitelist
TIKTOK_NICK = sys.argv[1] if len(sys.argv) > 1 else "@phh_0_011"

if TIKTOK_NICK not in WHITELIST:
    print(f"❌ {TIKTOK_NICK} não está na whitelist!")
    sys.exit(1)

print(f"✅ Conectando como {TIKTOK_NICK}")

app = Flask(__name__)
queue = []

client = TikTokLiveClient(unique_id=TIKTOK_NICK)

@client.on(ConnectEvent)
async def on_connect(event):
    print("✅ Conectado na live!")

@client.on(DisconnectEvent)
async def on_disconnect(event):
    print("❌ Desconectado da live.")

@client.on(CommentEvent)
async def on_comment(event):
    roblox_name = event.comment.strip()
    if " " in roblox_name:
        return
    print(f"🔥 CHEGOU: {roblox_name}")
    queue.append(roblox_name)

@app.route("/get")
def get_user():
    return jsonify({"user": queue.pop(0) if queue else None})

@app.route("/")
def home():
    return "OK"

@app.route("/test/<username>")
def test_user(username):
    queue.append(username)
    return jsonify({"status": "ok", "user": username})

def run_tiktok():
    try:
        client.run()
    except Exception as e:
        print(f"❌ Erro TikTok: {e}")

threading.Thread(target=run_tiktok, daemon=True).start()

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
