import sqlite3
import json
from pathlib import Path

# Imports de nos vues
from gestion_sauveteurs.view.login import lancer_login
from gestion_sauveteurs.view.administrateur import lancer_administrateur
from gestion_sauveteurs.view.gestionnaire import lancer_gestionnaire # <--- Importé
from gestion_sauveteurs.view.planning_public import lancer_planning_public # <--- Importé

from gestion_sauveteurs.connexion_réseaux import pair, charger_ips_machines
from gestion_sauveteurs.database import DatabaseManager

# =============================================================================
# CONFIGURATION
# =============================================================================

db_path = "../data/application.db"

# ... (Le reste du code réseau et fonctions internes reste identique) ...
# ... Copie tout ce qui concerne le réseau et les fonctions _appliquer_... ici ...
# Pour faire court, je ne remets que la fonction main() modifiée ci-dessous :

# ... (Assure-toi de garder les fonctions traitement_message, ajouter_sauveteur, etc.) ...

# =============================================================================
# . POINT D'ENTRÉE PRINCIPAL (MAIN)
# =============================================================================

def main():
    """Point d'entrée principal de l'application.

    Cette fonction orchestre le lancement :
    1. Initialisation de la base de données.
    2. Affichage de la fenêtre de login (bloquante).
    3. Lancement de l'interface principale selon le rôle utilisateur.
    """
    print("Démarrage de l'application ---")
    
    # 1. Init BDD
    print("Vérification de la base de données...")
    db_manager = DatabaseManager()
    db_manager.initialiser()
    
    # 2. Login (Bloquant)
    print("Ouverture du login...")
    role_connecte = lancer_login()

    # 3. Navigation selon le rôle récupéré
    if role_connecte:
        print(f"Utilisateur connecté : {role_connecte}")
        
        if role_connecte == "administrateur":
            lancer_administrateur()
            
        elif role_connecte == "gestionnaire":
            # On lance maintenant la vraie fenêtre !
            lancer_gestionnaire()
            
        elif role_connecte == "lecture":
            # On lance le planning public
            lancer_planning_public()
            
    else:
        print("Aucune connexion (Fermeture).")

if __name__ == "__main__":
    main()