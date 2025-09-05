from flask import Flask, render_template, request, redirect, url_for

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
    return f"<h1>Willkommen im Spiel, {username}!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
