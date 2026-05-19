from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)
queue = []
client = TikTokLiveClient(unique_id="@weverti04")

@client.on(CommentEvent)
async def on_comment(event):
    roblox_name = event.comment.strip()
    if " " in roblox_name:
        return
    queue.append(roblox_name)
    print(f"{roblox_name} entrou no jogo!")

@app.route("/get")
def get_user():
    if len(queue) > 0:
        return jsonify({"user": queue.pop(0)})
    return jsonify({"user": None})

@app.route("/test/<username>")
def test_user(username):
    queue.append(username)
    return jsonify({"status": "ok", "user": username})

threading.Thread(target=lambda: app.run(port=5000), daemon=True).start()
client.run()