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


# Lire le fichier de configuration
with open("gestion_sauveteurs/config.json") as fichier_config:
    configuration = json.load(fichier_config)

# Fonction qui applique les mises à jour reçues
def appliquer_mise_à_jour(mise_à_jour):
    print("Mise à jour reçue :", mise_à_jour)
    # Ici : mettre à jour la base de données et rafraîchir l'interface PyQt

# Initialiser le réseau P2P
reseau = RéseauPairÀPair(configuration['machines'], port=configuration['port'], fonction_mise_à_jour=appliquer_mise_à_jour)

# Exemple : envoyer une mise à jour quand le planning est modifié localement
mise_à_jour_exemple = {
    "type": "mise_à_jour_planning",
    "id_sauveteur": 3,
    "timestamp": "2025-11-12 10:30",
    "statut": "sous_terre"
}
reseau.diffuser_mise_à_jour(mise_à_jour_exemple)

