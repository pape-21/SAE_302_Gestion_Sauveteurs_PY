def main():
    import sqlite3
    from pathlib import Path
    import json
    from gestion_sauveteurs.connexion_réseaux import RéseauPairÀPair

    db_path = Path("data/database.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if db_path.stat().st_size == 0:
        with open("data/script_base_de_donne.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        cur.executescript(sql_script)
        conn.commit()
        print("Base de données initialisée.")

    conn.close()
    print("Application prête à fonctionner")
 
    #Chargement du fichier de configuration réseau
    
    chemin_config = Path("gestion_sauveteurs/config.json")
    fichier = open(chemin_config, "r", encoding="utf-8")
    contenu = fichier.read()
    fichier.close()
    configuration = json.loads(contenu)

    # Liste des autres machines du réseau
    if "machines" in configuration:
        liste_machines = configuration["machines"]
    else:
        liste_machines = []
        print("Aucune machine distante définie dans config.json")
 # Mise en place du système réseau pair-à-pair

    def traitement_message(message, adresse):
        """
        Fonction appelée automatiquement lorsque cette machine
        reçoit un message réseau JSON provenant d’une autre machine.
        """
        action = message.get("action")
        donnees = message.get("donnees")

        # Traitement des deltas
        if action == "ajout_sauveteur":
            appliquer_ajout_sauveteur(donnees)

        if action == "modification_sauveteur":
            appliquer_modification_sauveteur(donnees)

        if action == "suppression_sauveteur":
            appliquer_suppression_sauveteur(donnees)

        if action == "ajout_mission":
            appliquer_ajout_mission(donnees)

        if action == "modification_mission":
            appliquer_modification_mission(donnees)

        if action == "suppression_mission":
            appliquer_suppression_mission(donnees)

        print("Mise à jour reçue depuis", adresse)

    # Création du réseau pair-à-pair
    reseau = RéseauPairÀPair(
        liste_ips=liste_machines,
        port=5002,
        fonction_rappel=traitement_message
    )

    # Démarrage du serveur réseau (écoute des autres machines)
    reseau.demarrer_serveur()

    print("Synchronisation réseau activée.")
    print("Cette machine écoute maintenant les modifications du planning.")

    # Fonctions locales pour appliquer les déltas reçus


    def appliquer_ajout_sauveteur(donnees):
        connexion = sqlite3.connect("data/database.db")
        curseur = connexion.cursor()
        curseur.execute(
            "INSERT INTO sauveteurs (nom, prenom, departement, specialite) VALUES (?, ?, ?, ?, ?)",
            (
                donnees["nom"],
                donnees["prenom"],
                donnees["departement"],
                donnees["specialite"],
            )
        )
        connexion.commit()
        connexion.close()

    def appliquer_modification_sauveteur(donnees):
        connexion = sqlite3.connect("data/database.db")
        curseur = connexion.cursor()
        curseur.execute(
            "UPDATE sauveteurs SET nom=?, prenom=?, departement=?, specialite=?, engagement_datetime=? WHERE id=?",
            (
                donnees["nom"],
                donnees["prenom"],
                donnees["departement"],
                donnees["specialite"],
                donnees["engagement_datetime"],
                donnees["id"]
            )
        )
        connexion.commit()
        connexion.close()

    def appliquer_suppression_sauveteur(donnees):
        connexion = sqlite3.connect("data/database.db")
        curseur = connexion.cursor()
        curseur.execute("DELETE FROM sauveteurs WHERE id=?", (donnees["id"],))
        connexion.commit()
        connexion.close()

    def appliquer_ajout_mission(donnees):
        connexion = sqlite3.connect("data/database.db")
        curseur = connexion.cursor()
        curseur.execute(
            "INSERT INTO missions (sauveteur_id, debut, fin, type_mission, preparation) VALUES (?, ?, ?, ?, ?)",
            (
                donnees["sauveteur_id"],
                donnees["debut"],
                donnees["fin"],
                donnees["type_mission"],
                donnees["preparation"]
            )
        )
        connexion.commit()
        connexion.close()

    def appliquer_modification_mission(donnees):
        connexion = sqlite3.connect("data/database.db")
        curseur = connexion.cursor()
        curseur.execute(
            "UPDATE missions SET sauveteur_id=?, debut=?, fin=?, type_mission=?, preparation=? WHERE id=?",
            (
                donnees["sauveteur_id"],
                donnees["debut"],
                donnees["fin"],
                donnees["type_mission"],
                donnees["preparation"],
                donnees["id"]
            )
        )
        connexion.commit()
        connexion.close()

    def appliquer_suppression_mission(donnees):
        connexion = sqlite3.connect("data/database.db")
        curseur = connexion.cursor()
        curseur.execute("DELETE FROM missions WHERE id=?", (donnees["id"],))
        connexion.commit()
        connexion.close()
    
