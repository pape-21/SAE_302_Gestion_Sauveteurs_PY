import sqlite3
from gestion_sauveteurs.database import DatabaseManager

class SauveteurCRUD:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def ajouter(self, nom, prenom, departement, specialite):
        """Ajoute un nouveau sauveteur et retourne son ID."""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO sauveteur (nom, prenom, departement, specialite, statut)
            VALUES (?, ?, ?, ?, 'disponible')
            """
            cursor.execute(sql, (nom, prenom, departement, specialite))
            conn.commit()
            return cursor.lastrowid # On retourne l'ID créé
        except sqlite3.Error as e:
            print(f"Erreur d'ajout : {e}")
            return None
        finally:
            conn.close()

    def get_tous(self):
        """Récupère tous les sauveteurs sous forme de liste de dictionnaires."""
        conn = self.db_manager.get_connection()
        # Cette ligne permet d'avoir des résultats par nom de colonne (comme un dict)
        conn.row_factory = sqlite3.Row  
        cursor = conn.cursor()  
        
        try:
            cursor.execute("SELECT * FROM sauveteur")
            rows = cursor.fetchall()
            
            # Conversion en liste de dictionnaires pour faciliter le JSON plus tard
            liste_sauveteurs = [dict(row) for row in rows]
            return liste_sauveteurs
        except sqlite3.Error as e:
            print(f"Erreur de lecture : {e}")
            return []
        finally:
            conn.close()

    # Dans gestion_sauveteurs/crud/sauveteur.py
# ...

# Simule une fonction qui serait fournie par le contrôleur (Perceval)
# Pour l'instant, c'est une fonction vide que Perceval remplacera.
def NOTIFIER_RESEAU(payload):
    """Placeholder pour la fonction d'envoi réseau de Perceval."""
    # print(f"[NOTIFICATION SIMULÉE] Envoi du payload : {payload[:50]}...")
    pass

class SauveteurCRUD:
    # ... autres méthodes

    def update_statut(self, id_sauveteur, nouveau_statut):
        """Change le statut et notifie le réseau."""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Mise à jour de la BDD
            sql = "UPDATE sauveteur SET statut = ? WHERE id = ?"
            cursor.execute(sql, (nouveau_statut, id_sauveteur))
            success = cursor.rowcount > 0
            conn.commit()

            # 2. Notification si la mise à jour a eu lieu
            if success:
                # Récupérer les données mises à jour pour le payload
                cursor.execute("SELECT * FROM sauveteur WHERE id = ?", (id_sauveteur,))
                data = dict(cursor.fetchone())
                
                # Générer le JSON avec ton module
                from gestion_sauveteurs.utils.serialiseur import creer_payload_update
                
                payload = creer_payload_update("sauveteur", data)
                
                # C'est ici que tu passes la main à Perceval
                NOTIFIER_RESEAU(payload) 

            return success

        except sqlite3.Error as e:
            print(f"Erreur update : {e}")
            return False
        finally:
            conn.close()
    def supprimer(self, id_sauveteur):
        """Supprime un sauveteur"""
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