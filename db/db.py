import os
import sqlite3
from models.user import User
from models.game import Game
from models.highscore import Highscore

DB_PATH = 'zahlenraten.db'
def createTables():
    script_dir = os.path.dirname(__file__)  # Ordner von db.py
    sql_path = os.path.join(script_dir, "create_tables.sql")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open(sql_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

# --- CREATE FUNCTIONS ---

def createUser(user: User):
    createTables()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user (user_id, username, password) VALUES (?, ?, ?)",
        (user.user_id, user.username, user.password)
    )
    conn.commit()
    conn.close()

def createGame(game: Game):
    createTables()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO game (user_id, random_number, aktuelle_versuche) VALUES (?, ?, ?)",
        (game.user_id, game.random_number, game.aktuelle_versuche)
    )
    conn.commit()
    conn.close()

def createHighscore(highscore: Highscore):
    createTables()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO highscore (user_id, game_id, versuche) VALUES (?, ?, ?)",
        (highscore.user_id, highscore.game_id, highscore.versuche)
    )
    conn.commit()
    conn.close()

# --- ADD OR UPDATE FUNCTIONS ---

def addOrUpdateUser(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user (username, password)
        VALUES (?, ?)
        ON CONFLICT(username) DO UPDATE SET password=excluded.password
        """,
        (user.username, user.password)
    )
    conn.commit()
    conn.close()

def addOrUpdateGame(game: Game):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO game (game_id, user_id, random_number, aktuelle_versuche)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(game_id) DO UPDATE SET
            user_id=excluded.user_id,
            random_number=excluded.random_number,
            versuche=excluded.versuche
        """,
        (game.game_id, game.user_id, game.random_number, game.aktuelle_versuche)
    )
    conn.commit()
    conn.close()

def addOrUpdateHighscore(highscore: Highscore):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO highscore (highscore_id, user_id, game_id, versuche)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(highscore_id) DO UPDATE SET
            user_id=excluded.user_id,
            game_id=excluded.game_id,
            versuche=excluded.versuche
        """,
        (highscore.highscore_id, highscore.user_id, highscore.game_id, highscore.versuche)
    )
    conn.commit()
    conn.close()

# --- DELETE FUNCTIONS ---

def deleteUser(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE user_id = ?", (user.user_id,))
    conn.commit()
    conn.close()

def deleteGame(game: Game):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM game WHERE game_id = ?", (game.game_id,))
    conn.commit()
    conn.close()

def deleteHighscore(highscore: Highscore):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM highscore WHERE highscore_id = ?", (highscore.highscore_id,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM highscore")
    cursor.execute("DELETE FROM game")
    cursor.execute("DELETE FROM user")
    conn.commit()
    conn.close()

# --- DROP TABLE FUNCTIONS ---

def dropUserTable():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS user")
    conn.commit()
    conn.close()

def dropGameTable():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS game")
    conn.commit()
    conn.close()

def dropHighscoreTable():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS highscore")
    conn.commit()
    conn.close()