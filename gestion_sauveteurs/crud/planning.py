import sqlite3
from gestion_sauveteurs.database import DatabaseManager

class PlanningCRUD:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def ajouter_mission(self, sauveteur_id, heure_debut, heure_fin, mission):
        """
        Ajoute une entrée au planning (une mission ou un repos).
        Les heures doivent être au format ISO8601 (ex: 'YYYY-MM-DD HH:MM:SS').
        """
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO planning (sauveteur_id, heure_debut, heure_fin, statut_mission)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(sql, (sauveteur_id, heure_debut, heure_fin, mission))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erreur d'ajout de mission : {e}")
            return None
        finally:
            conn.close()

            
    def supprimer_mission(self, id_mission):
        """Supprime une mission du planning."""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM planning WHERE id = ?"
            cursor.execute(sql, (id_mission,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur suppression mission : {e}")
            return False
        finally:
            conn.close()

    def get_planning_global(self, date_operation):
        """
        Récupère toutes les entrées de planning pour la date donnée,
        en joignant le nom du sauveteur.
        """
        conn = self.db_manager.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # Assurez-vous que l'opération se fait sur les bonnes heures/dates
            sql = f"""
            SELECT p.*, s.nom, s.prenom, s.specialite
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
            
    # Ajoutez ici des méthodes pour update_mission et supprimer_mission
    # ...

    