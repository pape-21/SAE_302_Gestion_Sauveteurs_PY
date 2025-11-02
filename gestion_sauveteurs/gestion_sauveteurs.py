import sqlite3
from pathlib import Path

# Vérifie si la base existe déjà
db_path = Path("data/sauveteurs.db")

# Connexion (crée automatiquement le fichier s’il n’existe pas)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Si la base est vide, on exécute le script SQL
if db_path.stat().st_size == 0:
    with open("data/script_base_de_donne.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    cur.executescript(sql_script)
    conn.commit()
    print("Base de données initialisée.")

conn.close()
