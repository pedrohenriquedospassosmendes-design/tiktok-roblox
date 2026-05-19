from flask import Flask, jsonify
import threading
import os

from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent

app = Flask(__name__)

queue = []

client = TikTokLiveClient(unique_id="@weverti04")


# =========================
# TIKTOK EM THREAD
# =========================
def start_tiktok():
    @client.on(CommentEvent)
    async def on_comment(event):
        username = event.user.unique_id
        comment = event.comment.strip()

        print(f"{username}: {comment}")

        queue.append(comment)

    client.run()


threading.Thread(target=start_tiktok).start()


# =========================
# API
# =========================
@app.route("/get")
def get_user():
    if len(queue) > 0:
        return jsonify({"user": queue.pop(0)})

    return jsonify({"user": None})


@app.route("/")
def home():
    return "OK - TikTok Roblox rodando"


# =========================
# START FLASK (PRINCIPAL)
# =========================
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
