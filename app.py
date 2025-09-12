from flask import Flask, render_template, request, redirect, url_for, jsonify, session

from db.db import createTables, createUser
from models.user import User
from werkzeug.security import generate_password_hash
app = Flask(__name__)
createTables()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    payload = request.get_json(silent=True) or {}
    if not payload:
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
    else:
        username = (payload.get("username") or "").strip()
        password = payload.get("password") or ""

    if not username or not password:
        return jsonify({"status": "error", "message": "Benutzername und Passwort erforderlich"}), 400

    session["username"] = username
    return jsonify({"status": "success", "username": username})

@app.route("/game/<username>")
def game(username):
    return render_template("game.html", username=username)

@app.route("/success")
def success():
    return render_template("login_success.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        #if getUserByName(username) == []:

        if username and password:
            hashed_password = generate_password_hash(password)
            user = User(username, hashed_password)
            createUser(user)
            return redirect(url_for("index"))
        return redirect(url_for("register"))
    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)

