import sqlite3
from pathlib import Path

db_path = Path("data/database.db")

def ajouter_utilisateur(nom_utilisateur, mot_de_passe, profil, id_utilisateur=None):

    """
    Ajoute un nouvel utilisateur à la base de données.
    :param nom_utilisateur: Nom d'utilisateur
    :param mot_de_passe: Mot de passe
    :param profil: Rôle/Profil de l'utilisateur
    :param id_utilisateur: (Optionnel) ID à forcer; si None, SQLite gère l'auto-incrément
    :return: ID du nouvel utilisateur créé
    """

    connexion = sqlite3.connect(db_path)
    try:
        cursor = connexion.cursor()
        if id_utilisateur is None:
            cursor.execute(
                "INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, profil) VALUES (?, ?, ?)",
                (nom_utilisateur, mot_de_passe, profil)
            )
        else:
            cursor.execute(
                "INSERT INTO utilisateurs (id_utilisateur, nom_utilisateur, mot_de_passe, profil) VALUES (?, ?, ?, ?)",
                (id_utilisateur, nom_utilisateur, mot_de_passe, profil)
            )
        connexion.commit()
        return cursor.lastrowid
    finally:
        connexion.close()

if __name__ == "__main__":
    # Test d'ajout d'un utilisateur (sans fournir d'ID)
    user_id = ajouter_utilisateur("jdoe", "passwd", "administrateur")
    print("Utilisateur créé, id =", user_id)