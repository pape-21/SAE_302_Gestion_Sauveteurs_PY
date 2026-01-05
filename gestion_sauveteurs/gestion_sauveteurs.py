import sqlite3
import json
from pathlib import Path
from gestion_sauveteurs.connexion_réseaux import pair, charger_ips_machines
from gestion_sauveteurs.view.login import lancer_login
from gestion_sauveteurs.database import DatabaseManager
from gestion_sauveteurs.view.administrateur import lancer_administrateur

# =============================================================================
# CONFIGURATION
# =============================================================================

# Chemin relatif simple vers la base de données
db_path = "../data/application.db"

# =============================================================================
# 1. CONFIGURATION RÉSEAU & LOGIQUE MÉTIER
# =============================================================================

liste_machines = charger_ips_machines()
if not liste_machines:
    print("Aucune machine distante définie dans config.json (Mode local uniquement)")

# CALLBACK : applique les modifications reçues d'autres machines
def traitement_message(message, adresse):
    action = message.get("action")
    donnees = message.get("donnees")

    if action == "ajout_sauveteur":
        _appliquer_ajout_sauveteur(donnees)
    elif action == "modification_sauveteur":
        _appliquer_modification_sauveteur(donnees)
    elif action == "suppression_sauveteur":
        _appliquer_suppression_sauveteur(donnees)
    elif action == "ajout_planning":  # Renommé pour coller au SQL
        _appliquer_ajout_planning(donnees) 
    elif action == "modification_planning":
        _appliquer_modification_planning(donnees)
    elif action == "suppression_planning":
        _appliquer_suppression_planning(donnees)

    print(f"Mise à jour reçue depuis {adresse}")

# CRÉATION DU RÉSEAU
reseau = pair(
    liste_machines=liste_machines,
    fonction_mise_a_jour=traitement_message
)
print("Synchronisation réseau activée.")


def ajouter_sauveteur(nom, prenom, departement, specialite):
    # Correction : utilisation directe de la variable db_path
    connexion = sqlite3.connect(db_path) 
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO sauveteur (nom, prenom, departement, specialite) VALUES (?, ?, ?, ?)",
        (nom, prenom, departement, specialite)
    )
    id_nouveau = curseur.lastrowid
    connexion.commit()
    connexion.close()

    message = {
        "action": "ajout_sauveteur",
        "donnees": {
            "id": id_nouveau,
            "nom": nom,
            "prenom": prenom,
            "departement": departement,
            "specialite": specialite
        }
    }
    reseau.diffuser_mise_a_jour(message)

def modifier_sauveteur(id_sauveteur, nom, prenom, departement, specialite):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE sauveteur SET nom=?, prenom=?, departement=?, specialite=? WHERE id=?",
        (nom, prenom, departement, specialite, id_sauveteur)
    )
    connexion.commit()
    connexion.close()

    message = {
        "action": "modification_sauveteur",
        "donnees": {
            "id": id_sauveteur,
            "nom": nom,
            "prenom": prenom,
            "departement": departement,
            "specialite": specialite
        }
    }
    reseau.diffuser_mise_a_jour(message)

def supprimer_sauveteur(id_sauveteur):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM sauveteur WHERE id=?", (id_sauveteur,))
    connexion.commit()
    connexion.close()

    message = {
        "action": "suppression_sauveteur",
        "donnees": {"id": id_sauveteur}
    }
    reseau.diffuser_mise_a_jour(message)

def ajouter_mission(sauveteur_id, debut, fin, type_mission):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO planning (sauveteur_id, heure_debut, heure_fin, statut_mission) VALUES (?, ?, ?, ?)",
        (sauveteur_id, debut, fin, type_mission)
    )
    id_nouveau = curseur.lastrowid
    connexion.commit()
    connexion.close()

    message = {
        "action": "ajout_planning",
        "donnees": {
            "id": id_nouveau,
            "sauveteur_id": sauveteur_id,
            "heure_debut": debut,
            "heure_fin": fin,
            "statut_mission": type_mission
        }
    }
    reseau.diffuser_mise_a_jour(message)

def modifier_mission(id_mission, sauveteur_id, debut, fin, type_mission):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE planning SET sauveteur_id=?, heure_debut=?, heure_fin=?, statut_mission=? WHERE id=?",
        (sauveteur_id, debut, fin, type_mission, id_mission)
    )
    connexion.commit()
    connexion.close()

    message = {
        "action": "modification_planning",
        "donnees": {
            "id": id_mission,
            "sauveteur_id": sauveteur_id,
            "heure_debut": debut,
            "heure_fin": fin,
            "statut_mission": type_mission
        }
    }
    reseau.diffuser_mise_a_jour(message)

def supprimer_mission(id_mission):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM planning WHERE id=?", (id_mission,))
    connexion.commit()
    connexion.close()

    message = {
        "action": "suppression_planning",
        "donnees": {"id": id_mission}
    }
    reseau.diffuser_mise_a_jour(message)

#  FONCTIONS INTERNES POUR LES MESSAGES REÇUS (Mise à jour locale)
def _appliquer_ajout_sauveteur(donnees):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT OR IGNORE INTO sauveteur (id, nom, prenom, departement, specialite) VALUES (?, ?, ?, ?, ?)",
        (donnees["id"], donnees["nom"], donnees["prenom"], donnees["departement"], donnees["specialite"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_modification_sauveteur(donnees):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE sauveteur SET nom=?, prenom=?, departement=?, specialite=? WHERE id=?",
        (donnees["nom"], donnees["prenom"], donnees["departement"], donnees["specialite"], donnees["id"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_suppression_sauveteur(donnees):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM sauveteur WHERE id=?", (donnees["id"],))
    connexion.commit()
    connexion.close()

def _appliquer_ajout_planning(donnees):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT OR IGNORE INTO planning (id, sauveteur_id, heure_debut, heure_fin, statut_mission) VALUES (?, ?, ?, ?, ?)",
        (donnees["id"], donnees["sauveteur_id"], donnees["heure_debut"], donnees["heure_fin"], donnees["statut_mission"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_modification_planning(donnees):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE planning SET sauveteur_id=?, heure_debut=?, heure_fin=?, statut_mission=? WHERE id=?",
        (donnees["sauveteur_id"], donnees["heure_debut"], donnees["heure_fin"], donnees["statut_mission"], donnees["id"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_suppression_planning(donnees):
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM planning WHERE id=?", (donnees["id"],))
    connexion.commit()
    connexion.close()

# =============================================================================
# . POINT D'ENTRÉE PRINCIPAL (MAIN)
# =============================================================================

def main():
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
            print("Ouvrir la fenêtre Gestionnaire ici")
            
        elif role_connecte == "lecture":
            print("Ouvrir la fenêtre Lecture Seule ici")
            
    else:
        print("Aucune connexion (Fermeture).")

if __name__ == "__main__":
    main()