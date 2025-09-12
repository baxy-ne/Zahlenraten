from flask import Flask, render_template, request, redirect, url_for

from db import db
from models.game import Game
from models.user import User
from uuid import uuid4
from werkzeug.security import generate_password_hash
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    username = request.form.get("username")
    if username:
        return redirect(url_for("game", username=username))
    return redirect(url_for("index"))

@app.route("/game/<username>")
def game(username):
    return render_template("game.html", username=username)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if username and password:
            hashed_password = generate_password_hash(password)
            user = User(username, hashed_password, str(uuid4()))
            return redirect(url_for("game", username=user.username))
        return redirect(url_for("register"))
    return render_template("register.html")

if __name__ == "__main__":
    user1 = User("arian","geheim")

    # 2. Neue Game-Instanz erstellen
    game1 = Game(
        aktuelle_versuche=0,  # Anfangsversuche
        random_number=42,  # zufällige Zahl z. B. für Zahlenraten
    )
    db.createUser(user1)
    # db.createGame(game1)

