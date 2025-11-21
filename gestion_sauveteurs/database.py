# Fichier : gestion_sauveteurs/database.py
import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_name="sauveteurs.db"):
        # On calcule le chemin pour que ça marche quel que soit l'endroit d'où on lance le script
        base_dir = Path(__file__).resolve().parent.parent
        self.db_path = base_dir / "data" / db_name
        self.sql_script_path = base_dir / "data" / "script_base_de_donne.sql"

    def get_connection(self):
        """Retourne une connexion active à la base"""
        return sqlite3.connect(self.db_path)

    def initialiser(self):
        """Crée les tables si elles n'existent pas via le script SQL"""
        # On s'assure que le dossier data existe
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if self.sql_script_path.exists():
                with open(self.sql_script_path, "r", encoding="utf-8") as f:
                    script = f.read()
                cursor.executescript(script)
                conn.commit()
                print(f"[OK] Base de données initialisée : {self.db_path}")
            else:
                print(f"[ERREUR] Script SQL introuvable : {self.sql_script_path}")
        except sqlite3.Error as e:
            print(f"[ERREUR SQL] {e}")
        finally:
            conn.close()