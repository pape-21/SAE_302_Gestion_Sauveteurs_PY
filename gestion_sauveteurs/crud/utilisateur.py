import sqlite3
from gestion_sauveteurs.database import DatabaseManager

class UtilisateurCRUD:
    """Classe de gestion des utilisateurs (Authentification et CRUD).
    """

    def __init__(self):
        """Initialise le gestionnaire de base de données.
        """
        self.gestionnaire_bdd = DatabaseManager()

    def verifier_connexion(self, identifiant_saisi, mdp_saisi):
        """Vérifie les identifiants pour la connexion.

        Args:
            identifiant_saisi (str): L'identifiant utilisateur.
            mdp_saisi (str): Le mot de passe utilisateur.

        Returns:
            str | None: Le rôle de l'utilisateur ('administrateur', etc.) ou None si échec.
        """
        connexion = self.gestionnaire_bdd.get_connection()
        curseur = connexion.cursor()
        try:
            requete = "SELECT role FROM utilisateur WHERE identifiant = ? AND mot_de_passe = ?"
            curseur.execute(requete, (identifiant_saisi, mdp_saisi))
            resultat = curseur.fetchone()
            
            if resultat:
                return resultat[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Erreur BDD : {e}")
            return None
        finally:
            connexion.close()

    def get_tous(self):
        """Récupère la liste de tous les utilisateurs.

        Returns:
            list[dict]: Une liste de dictionnaires représentant les utilisateurs.
        """
        conn = self.gestionnaire_bdd.get_connection()
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, identifiant, role FROM utilisateur")
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def ajouter_utilisateur(self, identifiant, mot_de_passe, role):
        """Ajoute un nouvel utilisateur.

        Args:
            identifiant (str): Le login souhaité.
            mot_de_passe (str): Le mot de passe.
            role (str): Le rôle ('administrateur', 'gestionnaire', 'lecture').

        Returns:
            bool: True si l'ajout a réussi, False sinon (ex: doublon).
        """
        conn = self.gestionnaire_bdd.get_connection()
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO utilisateur (identifiant, mot_de_passe, role) VALUES (?, ?, ?)"
            cursor.execute(sql, (identifiant, mot_de_passe, role))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False 
        except sqlite3.Error as e:
            print(f"Erreur ajout user: {e}")
            return False
        finally:
            conn.close()

    def supprimer(self, identifiant):
        """Supprime un utilisateur.

        Args:
            identifiant (str): L'identifiant de l'utilisateur à supprimer.

        Returns:
            bool: True si la suppression a réussi, False sinon.
        """
        conn = self.gestionnaire_bdd.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM utilisateur WHERE identifiant = ?", (identifiant,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()