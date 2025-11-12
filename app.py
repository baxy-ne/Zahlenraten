from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import random
from db.db import (createTables, createUser, getUserByName, createGame, 
                   createHighscore, getHighscore, getAllGames, getGameById)
from models.user import User
from models.game import Game
from models.highscore import Highscore
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev") 
createTables()

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("game", username=session["username"]))
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    payload = request.get_json(silent=True) or {}
    is_json_request = bool(payload)
    
    if not payload:
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
    else:
        username = (payload.get("username") or "").strip()
        password = payload.get("password") or ""

    if not username or not password:
        if is_json_request:
            return jsonify({"status": "error", "message": "Benutzername und Passwort erforderlich"}), 400
        return render_template("index.html", error="Benutzername oder Passwort falsch")

    # Benutzer aus Datenbank holen
    user_data = getUserByName(username)
    if not user_data:
        if is_json_request:
            return jsonify({"status": "error", "message": "Benutzer nicht gefunden"}), 404
        return render_template("index.html", error="Benutzername oder Passwort falsch")
    
    # Passwort überprüfen (Reihenfolge in DB: user_id, password, username)
    user_id, hashed_password, db_username = user_data
    if not check_password_hash(hashed_password, password):
        if is_json_request:
            return jsonify({"status": "error", "message": "Falsches Passwort"}), 401
        return render_template("index.html", error="Benutzername oder Passwort falsch")

    # Session setzen
    session["username"] = db_username
    session["user_id"] = user_id
    
    # Bei normalem Formular-Submit zur game.html weiterleiten
    if is_json_request:
        return jsonify({"status": "success", "username": username})
    else:
        return redirect(url_for("game", username=db_username))

@app.route("/game/<username>")
def game(username):
    if "username" not in session or session["username"] != username:
        return redirect(url_for("index"))
    return render_template("game.html", username=username)

@app.route("/api/game/start", methods=["POST"])
def start_game():
    """Startet ein neues Spiel"""
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Nicht eingeloggt"}), 401
    
    user_id = session["user_id"]
    
    # Neues Spiel erstellen
    game = Game(user_id=user_id, aktuelle_versuche=0)
    createGame(game)
    
    # Game ID aus Datenbank holen (letzte eingefügte ID)
    all_games = getAllGames()
    if all_games:
        game_id = all_games[-1][0]  # game_id ist das erste Element
        random_number = all_games[-1][2]  # random_number ist das dritte Element
        
        session["game_id"] = game_id
        session["random_number"] = random_number
        session["versuche"] = 0
        
        return jsonify({
            "status": "success",
            "message": "Spiel gestartet! Rate eine Zahl zwischen 1 und 100.",
            "game_id": game_id
        })
    
    return jsonify({"status": "error", "message": "Fehler beim Erstellen des Spiels"}), 500

@app.route("/api/game/guess", methods=["POST"])
def make_guess():
    """Verarbeitet einen Rateversuch"""
    if "user_id" not in session or "game_id" not in session:
        return jsonify({"status": "error", "message": "Kein aktives Spiel"}), 401
    
    data = request.get_json()
    guess = data.get("guess")
    
    if guess is None:
        return jsonify({"status": "error", "message": "Keine Zahl angegeben"}), 400
    
    try:
        guess = int(guess)
    except ValueError:
        return jsonify({"status": "error", "message": "Ungültige Zahl"}), 400
    
    if guess < 1 or guess > 100:
        return jsonify({"status": "error", "message": "Zahl muss zwischen 1 und 100 liegen"}), 400
    
    random_number = session["random_number"]
    session["versuche"] += 1
    versuche = session["versuche"]
    
    if guess == random_number:
        # Spiel gewonnen!
        game_id = session["game_id"]
        user_id = session["user_id"]
        
        # Highscore speichern
        highscore = Highscore(user_id=user_id, game_id=game_id, versuche=versuche)
        createHighscore(highscore)
        
        # Session aufräumen
        session.pop("game_id", None)
        session.pop("random_number", None)
        session.pop("versuche", None)
        
        return jsonify({
            "status": "success",
            "result": "correct",
            "message": f"🎉 Glückwunsch! Du hast die Zahl {random_number} in {versuche} Versuchen erraten!",
            "versuche": versuche
        })
    elif guess < random_number:
        return jsonify({
            "status": "success",
            "result": "too_low",
            "message": f"📈 Zu niedrig! Versuch {versuche}",
            "versuche": versuche
        })
    else:
        return jsonify({
            "status": "success",
            "result": "too_high",
            "message": f"📉 Zu hoch! Versuch {versuche}",
            "versuche": versuche
        })

@app.route("/api/highscores")
def get_highscores():
    """Gibt die Highscores zurück"""
    highscores = getHighscore()
    
    # Highscores formatieren
    formatted_scores = []
    for score in highscores:
        highscore_id, user_id, game_id, versuche = score
        # user_id ist eine UUID, wir müssen den User über getUserById holen
        from db.db import getUserById
        user_data = getUserById(user_id)
        
        formatted_scores.append({
            "user_id": user_id,
            "username": user_data[2] if user_data else "Unbekannt",  # username ist an Position 2 (user_id, password, username)
            "versuche": versuche,
            "game_id": game_id
        })
    
    # Nach Versuchen sortieren (weniger ist besser)
    formatted_scores.sort(key=lambda x: x["versuche"])
    
    return jsonify({"status": "success", "highscores": formatted_scores[:10]})

@app.route("/highscores")
def highscores_page():
    """Zeigt die Highscore-Seite"""
    return render_template("highscores.html")

@app.route("/success")
def success():
    return render_template("login_success.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        
        # Prüfen ob Username und Passwort vorhanden sind
        if not username or not password:
            return render_template("register.html", error="Benutzername und Passwort erforderlich")
        
        # Prüfen ob User bereits existiert
        if getUserByName(username):
            return render_template("register.html", error="Benutzername bereits vergeben")
        
        # User erstellen
        hashed_password = generate_password_hash(password)
        user = User(username, hashed_password)
        createUser(user)
        
        # Zur Login-Seite mit Erfolgsmeldung weiterleiten
        return render_template("index.html", success="Registrierung erfolgreich! Du kannst dich jetzt einloggen.")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Loggt den Benutzer aus"""
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

