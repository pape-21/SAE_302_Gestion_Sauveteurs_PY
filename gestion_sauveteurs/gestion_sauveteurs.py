import sqlite3
import json
from pathlib import Path

# --- IMPORTS VUES (POUR OUVRIR LES FENÊTRES) ---
from gestion_sauveteurs.view.login import lancer_login
from gestion_sauveteurs.view.administrateur import lancer_administrateur
from gestion_sauveteurs.view.gestionnaire import lancer_gestionnaire 
from gestion_sauveteurs.view.planning_public import lancer_planning_public 

# --- IMPORTS RÉSEAU & BDD ---
from gestion_sauveteurs.connexion_réseaux import pair, envoyer_message
from gestion_sauveteurs.database import DatabaseManager

# =============================================================================
# CONFIGURATION
# =============================================================================

# On calcule le chemin absolu pour éviter les erreurs de "fichier introuvable"
BASE_DIR = Path(__file__).resolve().parent.parent
# IMPORTANT : On s'aligne sur le nom utilisé dans database.py (sauveteurs.db)
db_path = BASE_DIR / "data" / "sauveteurs.db"

# Variable globale pour stocker les connexions réseaux actives
reseau_sockets = []

# =============================================================================
# 1. LOGIQUE RÉSEAU (RÉCEPTION & ENVOI)
# =============================================================================

def traitement_message(message, adresse_ip):
    """Callback : Appelé quand on REÇOIT un message d'une autre machine."""
    print(f"[SYNC] Mise à jour reçue de {adresse_ip} : {message.get('action')}")
    
    action = message.get("action")
    donnees = message.get("donnees")

    try:
        # On applique la modification en local SANS renvoyer de message (pour éviter une boucle infinie)
        if action == "ajout_sauveteur":
            _appliquer_ajout_sauveteur(donnees)
        elif action == "modification_sauveteur":
            _appliquer_modification_sauveteur(donnees)
        elif action == "suppression_sauveteur":
            _appliquer_suppression_sauveteur(donnees)
        elif action == "ajout_planning":
            _appliquer_ajout_planning(donnees) 
        elif action == "modification_planning":
            _appliquer_modification_planning(donnees)
        elif action == "suppression_planning":
            _appliquer_suppression_planning(donnees)
            
    except Exception as e:
        print(f"[SYNC ERROR] Impossible d'appliquer la mise à jour : {e}")


# =============================================================================
# 2. FONCTIONS CRUD PUBLIQUES (ACTION LOCALE + DIFFUSION RÉSEAU)
# =============================================================================

def ajouter_sauveteur(nom, prenom, departement, specialite):
    """Ajoute en BDD locale ET envoie l'info au réseau."""
    # 1. Action Locale
    conn = sqlite3.connect(db_path) 
    cur = conn.cursor()
    cur.execute("INSERT INTO sauveteur (nom, prenom, departement, specialite) VALUES (?, ?, ?, ?)",
                (nom, prenom, departement, specialite))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()

    # 2. Diffusion Réseau
    payload = {
        "action": "ajout_sauveteur",
        "donnees": {
            "id": new_id, "nom": nom, "prenom": prenom,
            "departement": departement, "specialite": specialite
        }
    }
    envoyer_message(payload, reseau_sockets)

def modifier_sauveteur(id_sauveteur, nom, prenom, departement, specialite):
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE sauveteur SET nom=?, prenom=?, departement=?, specialite=? WHERE id=?",
                 (nom, prenom, departement, specialite, id_sauveteur))
    conn.commit()
    conn.close()

    payload = {
        "action": "modification_sauveteur",
        "donnees": { "id": id_sauveteur, "nom": nom, "prenom": prenom, 
                     "departement": departement, "specialite": specialite }
    }
    envoyer_message(payload, reseau_sockets)

def supprimer_sauveteur(id_sauveteur):
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE FROM sauveteur WHERE id=?", (id_sauveteur,))
    conn.commit()
    conn.close()

    payload = {
        "action": "suppression_sauveteur",
        "donnees": {"id": id_sauveteur}
    }
    envoyer_message(payload, reseau_sockets)

def ajouter_mission(sauveteur_id, debut, fin, type_mission):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO planning (sauveteur_id, heure_debut, heure_fin, statut_mission) VALUES (?, ?, ?, ?)",
                (sauveteur_id, debut, fin, type_mission))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()

    payload = {
        "action": "ajout_planning",
        "donnees": { "id": new_id, "sauveteur_id": sauveteur_id, 
                     "heure_debut": debut, "heure_fin": fin, "statut_mission": type_mission }
    }
    envoyer_message(payload, reseau_sockets)

def modifier_mission(id_mission, sauveteur_id, debut, fin, type_mission):
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE planning SET sauveteur_id=?, heure_debut=?, heure_fin=?, statut_mission=? WHERE id=?",
                 (sauveteur_id, debut, fin, type_mission, id_mission))
    conn.commit()
    conn.close()

    payload = {
        "action": "modification_planning",
        "donnees": { "id": id_mission, "sauveteur_id": sauveteur_id, 
                     "heure_debut": debut, "heure_fin": fin, "statut_mission": type_mission }
    }
    envoyer_message(payload, reseau_sockets)

def supprimer_mission(id_mission):
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE FROM planning WHERE id=?", (id_mission,))
    conn.commit()
    conn.close()

    payload = {
        "action": "suppression_planning",
        "donnees": {"id": id_mission}
    }
    envoyer_message(payload, reseau_sockets)


# =============================================================================
# 3. FONCTIONS INTERNES (JUSTE BDD, PAS DE RÉSEAU)
# =============================================================================

def _appliquer_ajout_sauveteur(d):
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT OR IGNORE INTO sauveteur (id, nom, prenom, departement, specialite) VALUES (?, ?, ?, ?, ?)",
                 (d['id'], d['nom'], d['prenom'], d['departement'], d['specialite']))
    conn.commit()
    conn.close()

def _appliquer_modification_sauveteur(d):
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE sauveteur SET nom=?, prenom=?, departement=?, specialite=? WHERE id=?",
                 (d['nom'], d['prenom'], d['departement'], d['specialite'], d['id']))
    conn.commit()
    conn.close()

def _appliquer_suppression_sauveteur(d):
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE FROM sauveteur WHERE id=?", (d['id'],))
    conn.commit()
    conn.close()

def _appliquer_ajout_planning(d):
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT OR IGNORE INTO planning (id, sauveteur_id, heure_debut, heure_fin, statut_mission) VALUES (?, ?, ?, ?, ?)",
                 (d['id'], d['sauveteur_id'], d['heure_debut'], d['heure_fin'], d['statut_mission']))
    conn.commit()
    conn.close()

def _appliquer_modification_planning(d):
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE planning SET sauveteur_id=?, heure_debut=?, heure_fin=?, statut_mission=? WHERE id=?",
                 (d['sauveteur_id'], d['heure_debut'], d['heure_fin'], d['statut_mission'], d['id']))
    conn.commit()
    conn.close()

def _appliquer_suppression_planning(d):
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE FROM planning WHERE id=?", (d['id'],))
    conn.commit()
    conn.close()


# =============================================================================
# . POINT D'ENTRÉE PRINCIPAL (MAIN)
# =============================================================================

def main():
    """Point d'entrée principal de l'application."""
    global reseau_sockets

    print("--- Démarrage de l'application ---")
    
    # 1. Init BDD
    print("Vérification de la base de données...")
    db_manager = DatabaseManager()
    db_manager.initialiser()
    
    # 2. Init RÉSEAU (Serveur + Client)
    # On passe 'traitement_message' pour qu'il soit appelé quand on reçoit quelque chose
    print("[RESEAU] Initialisation...")
    reseau_sockets = pair(callback_mise_a_jour=traitement_message)
    
    # 3. Login (Bloquant)
    print("Ouverture du login...")
    role_connecte = lancer_login()

    # 4. Navigation selon le rôle
    if role_connecte:
        print(f"Utilisateur connecté : {role_connecte}")
        
        if role_connecte == "administrateur":
            lancer_administrateur()
            
        elif role_connecte == "gestionnaire":
            # Cette fois, on lance la vraie fenêtre !
            lancer_gestionnaire()
            
        elif role_connecte == "lecture":
            lancer_planning_public()
            
    else:
        print("Aucune connexion (Fermeture).")

if __name__ == "__main__":
    main()