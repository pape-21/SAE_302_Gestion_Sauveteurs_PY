# Fichier : test_pape.py (A la racine du projet)
from gestion_sauveteurs.database import DatabaseManager
import sqlite3

def main():
    print("--- Démarrage du test Backend (Pape) ---\n")

    # 1. Instanciation du gestionnaire
    db_manager = DatabaseManager("sauveteurs.db")

    # 2. Initialisation (Création des tables)
    print("1. Lancement de l'initialisation...")
    db_manager.initialiser()

    # 3. Test rapide : Est-ce qu'on peut écrire dedans ?
    print("\n2. Test d'insertion d'un sauveteur...")
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    try:
        # On insère un sauveteur bidon
        cursor.execute("""
            INSERT INTO sauveteur (nom, prenom, departement, specialite, statut)
            VALUES (?, ?, ?, ?, ?)
        """, ("Verdon", "Vincent", "07", "gestion", "disponible"))
        
        conn.commit()
        print("   -> Sauveteur inséré avec succès.")

        # 4. Test rapide : Est-ce qu'on peut lire ?
        print("\n3. Vérification (Lecture)...")
        cursor.execute("SELECT * FROM sauveteur ORDER BY id DESC LIMIT 1")
        sauveteur = cursor.fetchone()
        print(f"   -> Donnée récupérée : {sauveteur}")

    except sqlite3.Error as error:
        print(f"   -> Erreur durant le test : {error}")
    finally:
        conn.close()

    print("\n--- Fin du test ---")

if __name__ == "__main__":
    main()


    