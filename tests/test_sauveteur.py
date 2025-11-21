from gestion_sauveteurs.crud.sauveteur import SauveteurCRUD

def main():
    print("--- Test CRUD Sauveteur ---")
    crud = SauveteurCRUD()

    # 1. Test AJOUT
    print("\n1. Ajout de sauveteurs...")
    id1 = crud.ajouter("Behanzin", "Perceval", "86", "informatique")
    id2 = crud.ajouter("Gueye", "Sokhna", "75", "gestion")
    print(f"   -> Ajoutés avec ID : {id1} et {id2}")

    # 2. Test LECTURE
    print("\n2. Lecture de tous les sauveteurs...")
    sauveteurs = crud.get_tous()
    for s in sauveteurs:
        print(f"   -> {s['nom']} {s['prenom']} ({s['statut']})")

    # 3. Test UPDATE
    if id1:
        print(f"\n3. Mise à jour du statut de l'ID {id1} vers 'sous_terre'...")
        crud.update_statut(id1, "sous_terre")
        
        # Vérification
        liste = crud.get_tous()
        # On cherche notre sauveteur dans la liste
        sauveteur_modifie = next((s for s in liste if s['id'] == id1), None)
        print(f"   -> Nouveau statut : {sauveteur_modifie['statut']}")

    # 4. Test SUPPRESSION
    if id2:
        print(f"\n4. Suppression de l'ID {id2}...")
        crud.supprimer(id2)
        liste_finale = crud.get_tous()
        print(f"   -> Nombre de sauveteurs restants : {len(liste_finale)}")

if __name__ == "__main__":
    main()