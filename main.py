from flask import Flask, jsonify
import threading
import os

from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent

app = Flask(__name__)

queue = []

# TikTok LIVE (coloque seu @ aqui)
client = TikTokLiveClient(unique_id="@vinyyws")


# =========================
# TIKTOK EVENTO
# =========================
@client.on(CommentEvent)
async def on_comment(event):
    username = event.user.unique_id
    comment = event.comment.strip()

    print(f"{username}: {comment}")

    # aqui você decide o que entra no jogo
    queue.append(comment)


# =========================
# API PRO ROBLOX
# =========================
@app.route("/get")
def get_user():
    if len(queue) > 0:
        return jsonify({"user": queue.pop(0)})

    return jsonify({"user": None})


# =========================
# FLASK (RENDER FIX)
# =========================
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# =========================
# START
# =========================
threading.Thread(target=run_flask).start()
client.run()
