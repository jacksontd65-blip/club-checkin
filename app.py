from flask import Flask, render_template, request, jsonify
from datetime import datetime
import threading
import time

app = Flask(__name__)

present = set()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/checkin", methods=["POST"])
def checkin():
    name = request.form.get("name")
    present.add(name)
    return "OK"

@app.route("/checkout", methods=["POST"])
def checkout():
    name = request.form.get("name")
    present.discard(name)
    return "OK"

@app.route("/attendees")
def attendees():
    return jsonify(list(present))

def midnight_reset():
    while True:
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            present.clear()
            time.sleep(60)
        time.sleep(10)

threading.Thread(target=midnight_reset, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)