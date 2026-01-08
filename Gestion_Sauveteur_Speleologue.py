import sys
import sqlite3
from PyQt5.QtWidgets import QApplication

# On importe nos modules
from gestion_sauveteurs.database import DatabaseManager
# On importe la fenêtre principale (Gestionnaire) au lieu de l'ancienne fonction
from gestion_sauveteurs.view.login import Gestionnaire 
from gestion_sauveteurs.connexion_réseaux import pair, charger_ips_machines

def main():
    print("--- Démarrage de l'application (PyQt5) ---")
    
    # 1. Initialisation de la Base de Données
    print("[APP] Vérification de la base de données...")
    db_manager = DatabaseManager()
    db_manager.initialiser()
    
    # 2. Configuration du Réseau (Optionnel pour l'instant mais prêt)
    liste_machines = charger_ips_machines()
    if not liste_machines:
        print("[RESEAU] Mode local uniquement (pas de machines dans config.json)")
    
    # 3. Lancement de l'interface graphique
    print("[APP] Ouverture de la fenêtre principale...")
    
    # Nécessaire pour toute application PyQt5
    app = QApplication(sys.argv)
    
    # On instancie la fenêtre principale qui contient le Login
    fenetre_principale = Gestionnaire()
    fenetre_principale.show()
    
    # On lance la boucle événementielle
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()