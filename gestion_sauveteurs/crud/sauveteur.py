import sqlite3
from gestion_sauveteurs.database import DatabaseManager

# Fonction utilitaire pour le réseau (Perceval) 
def NOTIFIER_RESEAU(payload):
    """Fonction  pour simuler l'envoi réseau.

    Args:
        payload (str): Le message JSON à envoyer.

    Returns:
        None
    """
    pass

class SauveteurCRUD:
    
    """Classe de gestion des opérations CRUD pour les sauveteurs.
    """

    def __init__(self):
        """Initialise le gestionnaire de base de données.
        """
        self.db_manager = DatabaseManager()

    def get_tous(self):
        """Récupère tous les sauveteurs de la base de données.

        Returns:
            list[dict]: Une liste de dictionnaires contenant les infos des sauveteurs.
        """
        conn = self.db_manager.get_connection() 
        conn.row_factory = sqlite3.Row                                                
        cursor = conn.cursor()                                                        
        try:
            cursor.execute("SELECT * FROM sauveteur")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur de lecture : {e}")
            return []
        finally:
            conn.close()

    def ajouter(self, nom, prenom, departement, specialite):
        """Ajoute un nouveau sauveteur.

        Args:
            nom (str): Le nom du sauveteur.
            prenom (str): Le prénom du sauveteur.
            departement (str): Le département (ex: '75').
            specialite (str): La spécialité (ex: 'Plongée').

        Returns:
            int | None: L'ID du sauveteur créé, ou None en cas d'erreur.
        """
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO sauveteur (nom, prenom, departement, specialite, statut)
            VALUES (?, ?, ?, ?, 'disponible')
            """
            cursor.execute(sql, (nom, prenom, departement, specialite))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erreur d'ajout : {e}")
            return None
        finally:
            conn.close()

    def supprimer(self, id_sauveteur):
        """Supprime un sauveteur par son ID.

        Args:
            id_sauveteur (int | str): L'identifiant du sauveteur à supprimer.

        Returns:
            bool: True si la suppression a réussi, False sinon.
        """
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM sauveteur WHERE id = ?"
            cursor.execute(sql, (id_sauveteur,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur suppression : {e}")
            return False
        finally:
            conn.close()

    def update_statut(self, id_sauveteur, nouveau_statut):
        """Met à jour le statut et notifie le réseau.

        Args:
            id_sauveteur (int | str): L'ID du sauveteur.
            nouveau_statut (str): Le nouveau statut (ex: 'en mission').

        Returns:
            bool: True si la mise à jour a réussi, False sinon.
        """
        conn = self.db_manager.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            # 1. Mise à jour de la BDD
            sql = "UPDATE sauveteur SET statut = ? WHERE id = ?"
            cursor.execute(sql, (nouveau_statut, id_sauveteur))
            success = cursor.rowcount > 0
            conn.commit()

            # 2. Notification si la mise à jour a eu lieu
            if success:
                cursor.execute("SELECT * FROM sauveteur WHERE id = ?", (id_sauveteur,))
                row = cursor.fetchone()
                if row:
                    data = dict(row)
                    from gestion_sauveteurs.utils.serialiseur import creer_payload_update
                    payload = creer_payload_update("sauveteur", data)
                    NOTIFIER_RESEAU(payload) 

            return success

        except sqlite3.Error as e:
            print(f"Erreur update : {e}")
            return False
        finally:
            conn.close()