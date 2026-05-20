from flask import Flask, jsonify
import os
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent

app = Flask(__name__)
queue = []

client = TikTokLiveClient(unique_id="weverti04")


@client.on(CommentEvent)
async def on_comment(event):
    roblox_name = event.comment.strip()
    if " " in roblox_name:
        return
    print("🔥 CHEGOU:", roblox_name)
    queue.append(roblox_name)


@app.route("/get")
def get_user():
    return jsonify({"user": queue.pop(0) if queue else None})


@app.route("/")
def home():
    return "OK"


# =========================
# START TIKTOK (BACKGROUND)
# =========================
import threading
def run_tiktok():
    try:
        client.run()
    except Exception as e:
        print("❌ Erro TikTok:", e)
        
threading.Thread(target=client.run, daemon=True).start()


# =========================
# START FLASK (RENDER PRINCIPAL)
# =========================
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
