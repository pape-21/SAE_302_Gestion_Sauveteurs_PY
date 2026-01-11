import sqlite3
from gestion_sauveteurs.database import DatabaseManager

class PlanningCRUD:
    """Classe de gestion des opérations CRUD pour le planning (missions).
    """

    def __init__(self):
        """Initialise le gestionnaire de base de données.
        """
        self.db_manager = DatabaseManager()

    def get_tous_details(self):
        """Récupère le planning complet avec les détails des sauveteurs.

        Returns:
            list: Liste (id, nom_sauveteur, debut, fin, statut, lieu).
        """
        conn = self.db_manager.get_connection()
        try:
            cursor = conn.cursor()
            # Ajout de p.lieu dans la requête
            sql = """
                SELECT p.id, s.nom || ' ' || s.prenom as sauveteur_nom, 
                       p.heure_debut, p.heure_fin, p.statut_mission, p.lieu
                FROM planning p
                JOIN sauveteur s ON p.sauveteur_id = s.id
                ORDER BY p.heure_debut DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            conn.close()

    def get_planning_global(self, date_operation):
        """Récupère les missions pour une date donnée.

        Args:
            date_operation (str): La date au format 'YYYY-MM-DD'.

        Returns:
            list[dict]: Liste des missions avec détails du sauveteur.
        """
        conn = self.db_manager.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            # Ajout de p.lieu dans la requête
            sql = f"""
            SELECT p.id, p.heure_debut, p.heure_fin, p.statut_mission, p.lieu,
                   s.nom, s.prenom, s.specialite
            FROM planning p
            JOIN sauveteur s ON p.sauveteur_id = s.id
            WHERE p.heure_debut LIKE '{date_operation}%' 
            ORDER BY p.heure_debut
            """
            cursor.execute(sql)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erreur de lecture du planning : {e}")
            return []
        finally:
            conn.close()

    def ajouter_mission(self, sauveteur_id, heure_debut, heure_fin, mission, lieu=""):
        """Ajoute une mission au planning.

        Args:
            sauveteur_id (int): L'identifiant du sauveteur.
            heure_debut (str): Date et heure de début.
            heure_fin (str): Date et heure de fin.
            mission (str): Le statut ou nom de la mission.
            lieu (str, optional): Le lieu de la mission. Par défaut "".

        Returns:
            int: L'ID de la mission créée ou None en cas d'erreur.
        """
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO planning (sauveteur_id, heure_debut, heure_fin, statut_mission, lieu)
            VALUES (?, ?, ?, ?, ?)
            """
            # On passe le lieu dans la requête
            cursor.execute(sql, (sauveteur_id, heure_debut, heure_fin, mission, lieu))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erreur ajout mission: {e}")
            return None
        finally:
            conn.close()

    def supprimer_mission(self, id_mission):
        """Supprime une mission du planning.

        Args:
            id_mission (int | str): L'ID de la mission à supprimer.

        Returns:
            bool: True si la suppression a réussi, False sinon.
        """
        conn = self.db_manager.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM planning WHERE id=?", (id_mission,))
            conn.commit()
            return cursor.rowcount > 0          
        except sqlite3.Error as e:
            print(f"Erreur suppression mission : {e}")
            return False
        finally:
            conn.close()