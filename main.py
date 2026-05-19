from flask import Flask, jsonify
import os
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent

app = Flask(__name__)
queue = []

client = TikTokLiveClient(unique_id="nandox.ff1")


@client.on(CommentEvent)
async def on_comment(event):
    print("🔥 CHEGOU COMMENT:", event.comment)
    queue.append(event.comment)


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
threading.Thread(target=client.run, daemon=True).start()


# =========================
# START FLASK (RENDER PRINCIPAL)
# =========================
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
