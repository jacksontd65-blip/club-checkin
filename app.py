from flask import Flask, render_template, request, jsonify
from datetime import datetime
import threading
import time
from datetime import datetime

app = Flask(__name__)

present = set()
last_reset_date = datetime.now().date()

def check_reset():
    global present, last_reset_date
    today = datetime.now().date()
    if today != last_reset_date:
        present.clear()
        last_reset_date = today

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/checkin", methods=["POST"])
def checkin():
    check_reset()
    name = request.form.get("name")
    present.add(name)
    return "OK"

@app.route("/checkout", methods=["POST"])
def checkout():
    check_reset()
    name = request.form.get("name")
    present.discard(name)
    return "OK"

@app.route("/attendees")
def attendees():
    check_reset()
    return jsonify(list(present))

@app.route("/clear", methods=["POST"])
def clear():
    global present
    present.clear()
    return "OK"

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
