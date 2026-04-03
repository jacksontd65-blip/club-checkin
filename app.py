from flask import Flask, render_template, request, jsonify
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
    check_reset()
    return render_template("index.html")


@app.route("/checkin", methods=["POST"])
def checkin():
    check_reset()
    name = request.form.get("name")

    if name:
        present.add(name.strip())

    return "OK"


@app.route("/checkout", methods=["POST"])
def checkout():
    check_reset()
    name = request.form.get("name")

    if name:
        present.discard(name.strip())

    return "OK"


@app.route("/attendees")
def attendees():
    check_reset()
    return jsonify(sorted(list(present)))


@app.route("/clear", methods=["POST"])
def clear():
    global present
    present.clear()
    return "OK"


@app.route("/ping")
def ping():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
