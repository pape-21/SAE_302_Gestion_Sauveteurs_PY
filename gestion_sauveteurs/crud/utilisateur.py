import sqlite3
from gestion_sauveteurs.database import DatabaseManager

class UtilisateurCRUD:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def ajouter_utilisateur(self, identifiant, mot_de_passe, role):
        """
        Crée un nouvel utilisateur.
        Roles possibles : 'administrateur', 'gestionnaire', 'lecture'
        """
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO utilisateur (identifiant, mot_de_passe, role) VALUES (?, ?, ?)"
            cursor.execute(sql, (identifiant, mot_de_passe, role))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Erreur : L'identifiant '{identifiant}' existe déjà.")
            return False
        except sqlite3.Error as e:
            print(f"Erreur SQL : {e}")
            return False
        finally:
            conn.close()

    def verifier_connexion(self, identifiant, mot_de_passe_saisi):
        """
        Vérifie le couple identifiant/mot de passe.
        Retourne le 'role' si c'est bon, sinon None.
        """
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            # On cherche l'utilisateur
            sql = "SELECT role FROM utilisateur WHERE identifiant = ? AND mot_de_passe = ?"
            cursor.execute(sql, (identifiant, mot_de_passe_saisi))
            result = cursor.fetchone()
            
            if result:
                return result[0] # On retourne le rôle (ex: 'admin')
            else:
                return None # Identifiant ou mot de passe incorrect
        except sqlite3.Error as e:
            print(f"Erreur connexion : {e}")
            return None
        finally:
            conn.close()

    def get_tous(self):
        """Pour l'admin : voir la liste des comptes"""
        conn = self.db_manager.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, identifiant, role FROM utilisateur")
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
            
    def supprimer(self, identifiant):
        """Supprime un utilisateur par son identifiant"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM utilisateur WHERE identifiant = ?", (identifiant,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()