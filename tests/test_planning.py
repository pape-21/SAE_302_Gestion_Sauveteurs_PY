from datetime import datetime, timedelta
from gestion_sauveteurs.crud.planning import PlanningCRUD
from gestion_sauveteurs.crud.sauveteur import SauveteurCRUD # On a besoin d'un sauveteur pour tester

def main():
    print("--- Test CRUD Planning ---")
    planning_crud = PlanningCRUD()
    sauveteur_crud = SauveteurCRUD()

    # Étape 1 : S'assurer d'avoir un sauveteur à affecter
    sauveteur_id = sauveteur_crud.ajouter("Trex", "Alan", "09", "communication")
    if not sauveteur_id:
        print("[ERREUR] Impossible de créer un sauveteur, vérifiez SauveteurCRUD.")
        return

    # Étape 2 : Définir des créneaux
    debut = datetime.now()
    fin = debut + timedelta(hours=3)
    
    debut_str = debut.strftime('%Y-%m-%d %H:%M:%S')
    fin_str = fin.strftime('%Y-%m-%d %H:%M:%S')
    date_jour = debut.strftime('%Y-%m-%d')

    # 3. Ajout d'une mission
    print(f"\n3. Ajout d'une mission pour le sauveteur ID {sauveteur_id}...")
    mission_id = planning_crud.ajouter_mission(
        sauveteur_id,
        debut_str,
        fin_str,
        "sous_terre"
    )
    print(f"   -> Mission ajoutée avec ID : {mission_id}")

    # 4. Lecture du planning global
    print(f"\n4. Lecture du planning pour la date {date_jour}...")
    planning = planning_crud.get_planning_global(date_jour)

    if planning:
        print(f"   [OK] {len(planning)} entrée(s) trouvée(s).")
# NOUVEAU CODE (Correction de la clé)
        print(f"   -> Mission : {planning[0]['statut_mission']} | Sauveteur : {planning[0]['prenom']} {planning[0]['nom']}")
    else:
        print("   [ERREUR] Aucune entrée de planning trouvée.")
        
    # Nettoyage
    sauveteur_crud.supprimer(sauveteur_id)

if __name__ == "__main__":
    main()