def main():
    import sqlite3
    from pathlib import Path

    db_path = Path("data/database.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if db_path.stat().st_size == 0:
        with open("data/script_base_de_donne.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        cur.executescript(sql_script)
        conn.commit()
        print("Base de données initialisée.")

    conn.close()
    print("Application prête à fonctionner")


