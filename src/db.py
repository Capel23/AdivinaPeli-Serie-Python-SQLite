import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "adivina.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)
    conn = get_conn()
    cur = conn.cursor()
    # Tabla películas/series
    cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT CHECK(type IN ('pelicula','serie')) NOT NULL,
        year INTEGER,
        synopsis TEXT
    );
    """)
    # Tabla pistas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        cost INTEGER NOT NULL DEFAULT 5,
        FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
    );
    """)
    # Tabla puntuaciones
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        score INTEGER NOT NULL,
        date TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def add_item(title, type_, year, synopsis, hints):
    """Agrega una película/serie con sus pistas"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (title, type, year, synopsis) VALUES (?, ?, ?, ?)",
                (title, type_, year, synopsis))
    item_id = cur.lastrowid
    for hint_text, cost in hints:
        cur.execute("INSERT INTO hints (item_id, text, cost) VALUES (?, ?, ?)",
                    (item_id, hint_text, cost))
    conn.commit()
    conn.close()

def save_score(player_name, score):
    """Guarda la puntuación del jugador"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (player_name, score, date) VALUES (?, ?, ?)",
                (player_name, score, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
