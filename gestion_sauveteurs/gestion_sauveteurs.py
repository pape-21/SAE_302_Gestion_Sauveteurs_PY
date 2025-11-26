# Gestion_Sauveteur_Speleologue.py
import sqlite3
import json
from gestion_sauveteurs.view.administrateur import lancer_administrateur
from gestion_sauveteurs.connexion_réseaux import pair, charger_ips_machines
from gestion_sauveteurs.view.login import lancer_login
from gestion_sauveteurs.database import DatabaseManager  # <--- NOUVEL IMPORT

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
    elif action == "ajout_mission":
        _appliquer_ajout_mission(donnees)
    elif action == "modification_mission":
        _appliquer_modification_mission(donnees)
    elif action == "suppression_mission":
        _appliquer_suppression_mission(donnees)

    print(f"Mise à jour reçue depuis {adresse}")

# CRÉATION DU RÉSEAU
reseau = pair(
    liste_machines=liste_machines,
    fonction_mise_a_jour=traitement_message
)
print("Synchronisation réseau activée.")

# =============================================================================
# 2. WRAPPERS CRUD (Base de données)
# =============================================================================

def ajouter_sauveteur(nom, prenom, departement, specialite):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO sauveteurs (nom, prenom, departement, specialite) VALUES (?, ?, ?, ?)",
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
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE sauveteurs SET nom=?, prenom=?, departement=?, specialite=? WHERE id=?",
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
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM sauveteurs WHERE id=?", (id_sauveteur,))
    connexion.commit()
    connexion.close()

    message = {
        "action": "suppression_sauveteur",
        "donnees": {"id": id_sauveteur}
    }
    reseau.diffuser_mise_a_jour(message)

def ajouter_mission(sauveteur_id, debut, fin, type_mission, preparation):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO missions (sauveteur_id, debut, fin, type_mission, preparation) VALUES (?, ?, ?, ?, ?)",
        (sauveteur_id, debut, fin, type_mission, preparation)
    )
    id_nouveau = curseur.lastrowid
    connexion.commit()
    connexion.close()

    message = {
        "action": "ajout_mission",
        "donnees": {
            "id": id_nouveau,
            "sauveteur_id": sauveteur_id,
            "debut": debut,
            "fin": fin,
            "type_mission": type_mission,
            "preparation": preparation
        }
    }
    reseau.diffuser_mise_a_jour(message)

def modifier_mission(id_mission, sauveteur_id, debut, fin, type_mission, preparation):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE missions SET sauveteur_id=?, debut=?, fin=?, type_mission=?, preparation=? WHERE id=?",
        (sauveteur_id, debut, fin, type_mission, preparation, id_mission)
    )
    connexion.commit()
    connexion.close()

    message = {
        "action": "modification_mission",
        "donnees": {
            "id": id_mission,
            "sauveteur_id": sauveteur_id,
            "debut": debut,
            "fin": fin,
            "type_mission": type_mission,
            "preparation": preparation
        }
    }
    reseau.diffuser_mise_a_jour(message)

def supprimer_mission(id_mission):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM missions WHERE id=?", (id_mission,))
    connexion.commit()
    connexion.close()

    message = {
        "action": "suppression_mission",
        "donnees": {"id": id_mission}
    }
    reseau.diffuser_mise_a_jour(message)

#  FONCTIONS INTERNES POUR LES MESSAGES REÇUS
def _appliquer_ajout_sauveteur(donnees):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT OR IGNORE INTO sauveteurs (id, nom, prenom, departement, specialite) VALUES (?, ?, ?, ?, ?)",
        (donnees["id"], donnees["nom"], donnees["prenom"], donnees["departement"], donnees["specialite"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_modification_sauveteur(donnees):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE sauveteurs SET nom=?, prenom=?, departement=?, specialite=? WHERE id=?",
        (donnees["nom"], donnees["prenom"], donnees["departement"], donnees["specialite"], donnees["id"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_suppression_sauveteur(donnees):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM sauveteurs WHERE id=?", (donnees["id"],))
    connexion.commit()
    connexion.close()

def _appliquer_ajout_mission(donnees):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT OR IGNORE INTO missions (id, sauveteur_id, debut, fin, type_mission, preparation) VALUES (?, ?, ?, ?, ?, ?)",
        (donnees["id"], donnees["sauveteur_id"], donnees["debut"], donnees["fin"], donnees["type_mission"], donnees["preparation"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_modification_mission(donnees):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE missions SET sauveteur_id=?, debut=?, fin=?, type_mission=?, preparation=? WHERE id=?",
        (donnees["sauveteur_id"], donnees["debut"], donnees["fin"], donnees["type_mission"], donnees["preparation"], donnees["id"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_suppression_mission(donnees):
    connexion = sqlite3.connect("data/database.db")
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM missions WHERE id=?", (donnees["id"],))
    connexion.commit()
    connexion.close()

# =============================================================================
# 3. POINT D'ENTRÉE PRINCIPAL (MAIN)
# =============================================================================

def main():
    print("--- Démarrage de l'application ---")
    
    # 1. Init BDD
    print("[APP] Vérification de la base de données...")
    db_manager = DatabaseManager()
    db_manager.initialiser()
    
    # 2. Login (Bloquant)
    print("[APP] Ouverture du login...")
    role_connecte = lancer_login()

    # 3. Navigation selon le rôle récupéré
    if role_connecte:
        print(f"[APP] Utilisateur connecté : {role_connecte}")
        
        if role_connecte == "administrateur":
            lancer_administrateur()
            
        elif role_connecte == "gestionnaire":
            print("[TODO] Ouvrir la fenêtre Gestionnaire ici")
            # lancer_gestionnaire()  <-- À créer plus tard
            
        elif role_connecte == "lecture":
            print("[TODO] Ouvrir la fenêtre Lecture Seule ici")
            
    else:
        print("[APP] Aucune connexion (Fermeture).")

if __name__ == "__main__":
    main()