import sqlite3
from pathlib import Path

class DatabaseManager:
    """Classe responsable de la gestion de la connexion à la base de données SQLite.

    Elle gère le chemin d'accès au fichier `.db` et l'exécution du script SQL
    d'initialisation lors du premier lancement.
    """

    def __init__(self, db_name="sauveteurs.db"):
        """Initialise le gestionnaire de base de données.

        Calcule automatiquement les chemins absolus pour éviter les erreurs 
        si le script est lancé depuis un autre dossier.

        Args:
            db_name (str, optional): Le nom du fichier de base de données. 
                Par défaut "sauveteurs.db".
        """
        # On calcule le chemin pour que ça marche quel que soit l'endroit d'où on lance le script 
        base_dir = Path(__file__).resolve().parent.parent
        self.db_path = base_dir / "data" / db_name
        self.sql_script_path = base_dir / "data" / "script_base_de_donne.sql"

    def get_connection(self):
        """Crée et retourne une connexion active à la base de données.

        Returns:
            sqlite3.Connection: Un objet connexion de `sqlite3` prêt à être utilisé.
        """
        return sqlite3.connect(self.db_path)

    def initialiser(self):
        """Initialise la structure de la base de données (Tables).

        Cette méthode vérifie si le dossier `data` existe (le crée sinon),
        puis lit et exécute le script SQL `script_base_de_donne.sql`.

        Returns:
            None
        """
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