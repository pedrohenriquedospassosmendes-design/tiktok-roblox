from flask import Flask, jsonify
import os
import threading
import sys
import traceback
import time
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent, DisconnectEvent, GiftEvent

WHITELIST = [
    "@phh_0_011",
]

TIKTOK_NICK = sys.argv[1] if len(sys.argv) > 1 else "@phh_0_011"

if TIKTOK_NICK not in WHITELIST:
    print(f"❌ {TIKTOK_NICK} não está na whitelist!")
    sys.exit(1)

print(f"✅ Conectando como {TIKTOK_NICK}")

app = Flask(__name__)
queue = []
gift_queue = []
rose_queue = []
ultimo_comentario = {}

client = TikTokLiveClient(
    unique_id=TIKTOK_NICK,
    timeout=10.0
)

@client.on(ConnectEvent)
async def on_connect(event):
    print("✅ Conectado na live!")

@client.on(DisconnectEvent)
async def on_disconnect(event):
    print("❌ Desconectado da live.")

@client.on(CommentEvent)
async def on_comment(event):
    try:
        roblox_name = event.comment.strip()
        if " " in roblox_name:
            return
        user_id = event.user_info.uid
        ultimo_comentario[user_id] = roblox_name
        print(f"🔥 CHEGOU: {roblox_name}")
        queue.append(roblox_name)
    except Exception as e:
        print(f"❌ Erro comment: {e}")

@client.on(GiftEvent)
async def on_gift(event):
    try:
        user_id = event.user_info.uid
        if event.gift.id == 5655:
            roblox_nick = ultimo_comentario.get(user_id)
            if roblox_nick:
                print(f"🍩 DONUT: {roblox_nick}")
                gift_queue.append(roblox_nick)
            else:
                print(f"🍩 DONUT mas sem nick comentado")
        elif event.gift.id == 5263:
            roblox_nick = ultimo_comentario.get(user_id)
            if roblox_nick:
                print(f"🌹 ROSA: {roblox_nick}")
                rose_queue.insert(0, roblox_nick)
            else:
                print(f"🌹 ROSA mas sem nick comentado")
    except Exception as e:
        print(f"❌ Erro gift: {e}")

@app.route("/get")
def get_user():
    return jsonify({"user": queue.pop(0) if queue else None})

@app.route("/gift")
def get_gift():
    return jsonify({"user": gift_queue.pop(0) if gift_queue else None})

@app.route("/rose")
def get_rose():
    return jsonify({"user": rose_queue.pop(0) if rose_queue else None})

@app.route("/")
def home():
    return "OK"

@app.route("/test/<username>")
def test_user(username):
    queue.append(username)
    return jsonify({"status": "ok", "user": username})

@app.route("/testgift/<username>")
def test_gift(username):
    gift_queue.append(username)
    return jsonify({"status": "ok", "user": username})

@app.route("/testrose/<username>")
def test_rose(username):
    rose_queue.insert(0, username)
    return jsonify({"status": "ok", "user": username})

def run_tiktok():
    while True:
        try:
            print("🔄 Tentando conectar no TikTok...")
            client.run()
        except Exception as e:
            print(f"❌ Erro TikTok: {type(e).__name__}: {e}")
            traceback.print_exc()
            print("🔄 Reconectando em 10 segundos...")
            time.sleep(10)

threading.Thread(target=run_tiktok, daemon=True).start()

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
