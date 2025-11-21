from gestion_sauveteurs.crud.utilisateur import UtilisateurCRUD

def main():
    print("--- Test CRUD Utilisateur & Connexion ---")
    crud = UtilisateurCRUD()

    # 1. Ajout d'utilisateurs
    print("\n1. Création des comptes...")
    crud.ajouter_utilisateur("chef", "1234", "gestionnaire")
    crud.ajouter_utilisateur("visiteur", "0000", "lecture")
    # Note : 'admin' est déjà créé par le script SQL normalement                           
    print("   -> Comptes créés.")

    # 2. Test de connexion RÉUSSI
    print("\n2. Test de connexion valide (chef / 1234)...")
    role = crud.verifier_connexion("chef", "1234")
    if role: 
        print(f"   [OK] Connexion réussie ! Rôle détecté : {role}")
    else:
        print("   [ERREUR] Connexion refusée (Bizarre...)")

    # 3. Test de connexion ÉCHOUÉ
    print("\n3. Test de connexion invalide (chef / mauvais_mot_de_passe)...")
    role_faux = crud.verifier_connexion("chef", "mauvais_mdp")
    if role_faux is None:
        print("   [OK] Connexion refusée correctement.")
    else:
        print("   [ERREUR] Il s'est connecté avec un mauvais mot de passe !")

    # 4. Liste des utilisateurs
    print("\n4. Liste des comptes en base :")
    users = crud.get_tous()
    for u in users:
        print(f"   -> {u['identifiant']} ({u['role']})")

if __name__ == "__main__":
    main()


