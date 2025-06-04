import sqlite3
import re

def processar_dados():
    conn = sqlite3.connect("projeto_rpa.db")
    cursor = conn.cursor()

    cursor.execute("SELECT code FROM cartas")
    codigos = cursor.fetchall()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dados_processados (
        code TEXT PRIMARY KEY,
        valido INTEGER
    )
    """)

    padrao = re.compile(r'^[2-9AJQK10]{1,2}[SHDC]$')

    for (codigo,) in codigos:
        valido = bool(padrao.match(codigo))
        cursor.execute("INSERT OR REPLACE INTO dados_processados VALUES (?, ?)", (codigo, int(valido)))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    processar_dados()