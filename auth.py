import sqlite3
from pathlib import Path

base = Path("data/database.db")

def se_connecter():
    """Demande les identifiants et renvoie le profil de l'utilisateur"""
    identifiant = input("Nom d'utilisateur : ").strip()
    mot_de_passe = input("Mot de passe : ").strip()

    # connexion à la base de données
    connexion = sqlite3.connect(base)
    curseur = connexion.cursor()

    # rechercher le profil correspondant
    curseur.execute(
        "SELECT profil FROM utilisateur WHERE identifiant=? AND mot_de_passe=?",
        (identifiant, mot_de_passe)
    )
    resultat = curseur.fetchone()
    connexion.close()

    if resultat:
        profil_utilisateur = resultat[0]
        print(f"Connecté en tant que {profil_utilisateur}")
        return profil_utilisateur
    else:
        print("Nom d'utilisateur ou mot de passe incorrect")
        return None
    
# -------------------------------------------------------------------
# MENUS SELON PROFILS
# -------------------------------------------------------------------

def afficher_menu_profil(profil):
    """Affiche le menu correspondant au rôle."""
    if profil == "lecture":
        menu_lecture()
    elif profil == "gestionnaire":
        menu_gestionnaire()
    elif profil == "admin":
        menu_admin()
    else:
        print("Profil inconnu !")


#PROFIL LECTURE
def menu_lecture():
    print("=== Menu LECTURE ===")
    print("1. Voir le planning")
    print("2. Voir les sauveteurs")
    print("3. Quitter")

    choix = input("Choix : ")
    if choix == "1":
        print("Affichage du planning (lecture seule).")
    elif choix == "2":
        print("Liste des sauveteurs (lecture seule).")
    else:
        print("Déconnexion.")


#PROFIL GESTIONNAIRE
def menu_gestionnaire():
    print("=== Menu GESTIONNAIRE ===")
    print("1. Voir le planning")
    print("2. Modifier le planning")
    print("3. Ajouter un sauveteur")
    print("4. Modifier un sauveteur")
    print("5. Quitter")

    choix = input("Choix : ")
    if choix == "1":
        print("Affichage du planning.")
    elif choix == "2":
        print("Modification du planning.")
    elif choix == "3":
        print("Ajout d'un sauveteur.")
    elif choix == "4":
        print("Modification d'un sauveteur.")
    else:
        print("Déconnexion.")


# PROFIL ADMIN
def menu_admin():
    print("=== Menu ADMIN ===")
    print("1. Voir le planning")
    print("2. Gérer les utilisateurs")
    print("3. Ajouter un utilisateur")
    print("4. Supprimer un utilisateur")
    print("5. Modifier un utilisateur")
    print("6. Quitter")

    choix = input("Choix : ")
    if choix == "1":
        print("Affichage du planning.")
    elif choix == "2":
        print("Gestion complète des utilisateurs.")
    elif choix == "3":
        print("Ajout d'un utilisateur.")
    elif choix == "4":
        print("Suppression d'un utilisateur.")
    elif choix == "5":
        print("Modification d'un utilisateur.")
    else:
        print("Déconnexion.")
