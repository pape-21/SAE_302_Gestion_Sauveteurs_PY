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

def traitement_message(message, adresse):
    """Callback appelé lorsqu'un message réseau est reçu.

    Cette fonction analyse l'action demandée (ajout, modification, suppression)
    et appelle la fonction interne correspondante pour mettre à jour la base locale.

    Args:
        message (dict): Le dictionnaire contenant 'action' et 'donnees'.
        adresse (str): L'adresse IP de l'émetteur (pour les logs).
    """
    action = message.get("action")
    donnees = message.get("donnees")

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

    print(f"Mise à jour reçue depuis {adresse}")

# CRÉATION DU RÉSEAU
reseau = pair(
    # NOTE: Si ta fonction 'pair' attend ces arguments, garde-les. 
    # Sinon adapte selon ton fichier connexion_réseaux.py
    # liste_machines=liste_machines, # <-- Vérifie si 'pair' prend des arguments
    # fonction_mise_a_jour=traitement_message
)
# ATTENTION: Dans le code précédent de connexion_réseaux, 'pair' ne prenait pas d'arguments
# et renvoyait une liste de sockets. Assure-toi que la logique ici correspond 
# à ta version de 'connexion_réseaux.py'.

print("Synchronisation réseau activée.")


def ajouter_sauveteur(nom, prenom, departement, specialite):
    """Ajoute un sauveteur en base locale et diffuse l'info au réseau.

    Args:
        nom (str): Nom du sauveteur.
        prenom (str): Prénom du sauveteur.
        departement (str): Département (ex: '75').
        specialite (str): Spécialité (ex: 'GRIMP').
    """
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
    # reseau.diffuser_mise_a_jour(message) # A décommenter quand intégré


def modifier_sauveteur(id_sauveteur, nom, prenom, departement, specialite):
    """Modifie un sauveteur existant et notifie le réseau.

    Args:
        id_sauveteur (int): ID du sauveteur à modifier.
        nom (str): Nouveau nom.
        prenom (str): Nouveau prénom.
        departement (str): Nouveau département.
        specialite (str): Nouvelle spécialité.
    """
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
    # reseau.diffuser_mise_a_jour(message)


def supprimer_sauveteur(id_sauveteur):
    """Supprime un sauveteur et notifie le réseau.

    Args:
        id_sauveteur (int): ID du sauveteur à supprimer.
    """
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM sauveteur WHERE id=?", (id_sauveteur,))
    connexion.commit()
    connexion.close()

    message = {
        "action": "suppression_sauveteur",
        "donnees": {"id": id_sauveteur}
    }
    # reseau.diffuser_mise_a_jour(message)


def ajouter_mission(sauveteur_id, debut, fin, type_mission):
    """Ajoute une mission au planning et diffuse l'info.

    Args:
        sauveteur_id (int): ID du sauveteur.
        debut (str): Date début (ISO).
        fin (str): Date fin (ISO).
        type_mission (str): Description.
    """
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
    # reseau.diffuser_mise_a_jour(message)


def modifier_mission(id_mission, sauveteur_id, debut, fin, type_mission):
    """Modifie une mission existante et notifie le réseau.

    Args:
        id_mission (int): ID de la mission.
        sauveteur_id (int): ID du sauveteur.
        debut (str): Nouvelle date début.
        fin (str): Nouvelle date fin.
        type_mission (str): Nouvelle description.
    """
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
    # reseau.diffuser_mise_a_jour(message)


def supprimer_mission(id_mission):
    """Supprime une mission et notifie le réseau.

    Args:
        id_mission (int): ID de la mission à supprimer.
    """
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM planning WHERE id=?", (id_mission,))
    connexion.commit()
    connexion.close()

    message = {
        "action": "suppression_planning",
        "donnees": {"id": id_mission}
    }
    # reseau.diffuser_mise_a_jour(message)


#  FONCTIONS INTERNES POUR LES MESSAGES REÇUS (Mise à jour locale)
def _appliquer_ajout_sauveteur(donnees):
    """Fonction interne : Applique un ajout reçu du réseau."""
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT OR IGNORE INTO sauveteur (id, nom, prenom, departement, specialite) VALUES (?, ?, ?, ?, ?)",
        (donnees["id"], donnees["nom"], donnees["prenom"], donnees["departement"], donnees["specialite"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_modification_sauveteur(donnees):
    """Fonction interne : Applique une modification reçue du réseau."""
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE sauveteur SET nom=?, prenom=?, departement=?, specialite=? WHERE id=?",
        (donnees["nom"], donnees["prenom"], donnees["departement"], donnees["specialite"], donnees["id"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_suppression_sauveteur(donnees):
    """Fonction interne : Applique une suppression reçue du réseau."""
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM sauveteur WHERE id=?", (donnees["id"],))
    connexion.commit()
    connexion.close()

def _appliquer_ajout_planning(donnees):
    """Fonction interne : Applique un ajout de mission reçu du réseau."""
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT OR IGNORE INTO planning (id, sauveteur_id, heure_debut, heure_fin, statut_mission) VALUES (?, ?, ?, ?, ?)",
        (donnees["id"], donnees["sauveteur_id"], donnees["heure_debut"], donnees["heure_fin"], donnees["statut_mission"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_modification_planning(donnees):
    """Fonction interne : Applique une modification de mission reçue du réseau."""
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE planning SET sauveteur_id=?, heure_debut=?, heure_fin=?, statut_mission=? WHERE id=?",
        (donnees["sauveteur_id"], donnees["heure_debut"], donnees["heure_fin"], donnees["statut_mission"], donnees["id"])
    )
    connexion.commit()
    connexion.close()

def _appliquer_suppression_planning(donnees):
    """Fonction interne : Applique une suppression de mission reçue du réseau."""
    connexion = sqlite3.connect(db_path)
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM planning WHERE id=?", (donnees["id"],))
    connexion.commit()
    connexion.close()

# =============================================================================
# . POINT D'ENTRÉE PRINCIPAL (MAIN)
# =============================================================================

def main():
    """Point d'entrée principal de l'application.

    Cette fonction orchestre le lancement :
    1. Initialisation de la base de données.
    2. Affichage de la fenêtre de login (bloquante).
    3. Lancement de l'interface principale selon le rôle utilisateur (Admin, Gestionnaire, etc.).
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
            # Ici tu devras instancier ta MainWindow du gestionnaire
            # Ex: app = QApplication(sys.argv); win = MainWindow(); win.show(); ...
            print("Ouvrir la fenêtre Gestionnaire ici")
            
        elif role_connecte == "lecture":
            print("Ouvrir la fenêtre Lecture Seule ici")
            
    else:
        print("Aucune connexion (Fermeture).")

if __name__ == "__main__":
    main()