import sqlite3
from pathlib import Path
db_path = Path("data/sauveteurs.db")
def ajouter_sauveteur(nom, prenom, departement, specialite):

    """
    Ajoute un nouveau sauveteur à la base de données.
    :param nom: Nom du sauveteur
    :param prenom: Prénom du sauveteur
    :param departement: Département de provenance
    :param specialite: Spécialité du sauveteur (parmi les valeurs autorisées)
    :return: ID du nouveau sauveteur créé
    """
    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()
    cursor.execute("""
        INSERT INTO sauveteurs (nom, prenom, departement, specialite)
        VALUES (?, ?, ?, ?)
    """, (nom, prenom, departement, specialite))
    connexion.commit()
    new_id = cursor.lastrowid
    connexion.close()
    return new_id



def supprimer_sauveteur(id_sauveteur):
    """
    Supprime un sauveteur de la base de données par son ID.
    :param id_sauveteur: ID du sauveteur à supprimer
    :return: Nombre de lignes supprimées (0 ou 1)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sauveteurs WHERE id_sauveteur = ?", (id_sauveteur,))
    conn.commit()
    sauveteur_supprime = cursor.rowcount
    conn.close()
    return sauveteur_supprime 

def modifier_sauveteur(id_sauveteur, nom=None, prenom=None, departement=None, specialite=None):
    """
    Modifie les informations d'un sauveteur existant.
    :param id_sauveteur: ID du sauveteur à modifier
    :param nom: Nouveau nom (optionnel)
    :param prenom: Nouveau prénom (optionnel)
    :param departement: Nouveau département (optionnel)
    :param specialite: Nouvelle spécialité (optionnel)
    :return: Nombre de lignes modifiées (0 ou 1)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Construire dynamiquement la requête de mise à jour
    champs = []
    valeurs = []
    if nom is not None:
        champs.append("nom = ?")
        valeurs.append(nom)
    if prenom is not None:
        champs.append("prenom = ?")
        valeurs.append(prenom)
    if departement is not None:
        champs.append("departement = ?")
        valeurs.append(departement)
    if specialite is not None:
        champs.append("specialite = ?")
        valeurs.append(specialite)

    valeurs.append(id_sauveteur)
    sql_query = f"UPDATE sauveteurs SET {', '.join(champs)} WHERE id_sauveteur = ?"

    cursor.execute(sql_query, valeurs)
    conn.commit()
    sauveteur_modifie = cursor.rowcount
    conn.close()
    return sauveteur_modifie

def lister_sauveteurs():
    """
    Récupère la liste de tous les sauveteurs dans la base de données.
    :return: Liste de dictionnaires représentant les sauveteurs
    """
    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()
    cursor.execute("SELECT id_sauveteur, nom, prenom, departement, specialite FROM sauveteurs")
    rows = cursor.fetchall()
    connexion.close()

    sauveteurs = []
    for row in rows:
        sauveteur = {
            "id_sauveteur": row[0],
            "nom": row[1],
            "prenom": row[2],
            "departement": row[3],
            "specialite": row[4]
        }
        sauveteurs.append(sauveteur)
    
    return sauveteurs

def obtenir_sauveteur(id_sauveteur):
    """
    Récupère les informations d'un sauveteur par son ID.
    :param id_sauveteur: ID du sauveteur à récupérer
    :return: Dictionnaire représentant le sauveteur ou None si non trouvé
    """
    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()
    cursor.execute("SELECT *FROM sauveteurs WHERE id_sauveteur = ?", (id_sauveteur,))
    row = cursor.fetchone()
    connexion.close()

    if row:
        sauveteur = {
            "id_sauveteur": row[0],
            "nom": row[1],
            "prenom": row[2],
            "departement": row[3],
            "specialite": row[4]
        }
        return sauveteur
    else:
        return None 


def rechercher_sauveteurs_par_specialite(specialite):
    """
    Recherche des sauveteurs par spécialité.
    :param specialite: Spécialité à rechercher
    :return: Liste de dictionnaires représentant les sauveteurs correspondants
    """
    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM sauveteurs WHERE specialite = ?", (specialite,))
    rows = cursor.fetchall()
    connexion.close()

    sauveteurs = []
    for row in rows:
        sauveteur = {
            "id_sauveteur": row[0],
            "nom": row[1],
            "prenom": row[2],
            "departement": row[3],
            "specialite": row[4]
        }
        sauveteurs.append(sauveteur)
    
    return sauveteurs

def compter_sauveteurs():
    """
    Compte le nombre total de sauveteurs dans la base de données.
    :return: Nombre total de sauveteurs
    """
    connexion = sqlite3.connect(db_path)
    cursor = connexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM sauveteurs")
    nbr_de_sauveteurs = cursor.fetchone()[0]
    conn.close()
    return nbr_de_sauveteurs
