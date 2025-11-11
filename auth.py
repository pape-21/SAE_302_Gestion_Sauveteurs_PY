import sqlite3

FICHIER_BD = "planning.db"

def se_connecter():
    """Demande les identifiants et renvoie le profil de l'utilisateur"""
    nom_utilisateur = input("Nom d'utilisateur : ").strip()
    mot_de_passe = input("Mot de passe : ").strip()

    # connexion à la base de données
    connexion = sqlite3.connect(FICHIER_BD)
    curseur = connexion.cursor()

    # rechercher le profil correspondant
    curseur.execute(
        "SELECT profil FROM utilisateurs WHERE nom_utilisateur=? AND mot_de_passe=?",
        (nom_utilisateur, mot_de_passe)
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
