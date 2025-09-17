PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user (
    user_id varchar(255),
    password TEXT,
    username TEXT
);

CREATE TABLE IF NOT EXISTS game (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id varchar(255),
    random_number INTEGER,
    aktuelle_versuche INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS highscore (
    highscore_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id varchar (255),
    game_id INTEGER,
    versuche INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id)
);