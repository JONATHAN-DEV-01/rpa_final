# coleta_dados.py
import requests
import sqlite3

def coletar_dados():
    url = "https://deckofcardsapi.com/api/deck/new/draw/?count=5"
    response = requests.get(url)
    data = response.json()
    cartas = data["cards"]

    conn = sqlite3.connect("projeto_rpa.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cartas (
        code TEXT PRIMARY KEY,
        value TEXT,
        suit TEXT,
        image TEXT
    )
    """)

    for carta in cartas:
        cursor.execute("INSERT OR REPLACE INTO cartas VALUES (?, ?, ?, ?)",
                       (carta["code"], carta["value"], carta["suit"], carta["image"]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    coletar_dados()

