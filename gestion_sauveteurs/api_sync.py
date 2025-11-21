# Dans un nouveau fichier : gestion_sauveteurs/api_sync.py

from gestion_sauveteurs.crud.sauveteur import SauveteurCRUD
from gestion_sauveteurs.crud.planning import PlanningCRUD
from gestion_sauveteurs.crud.utilisateur import UtilisateurCRUD

def traiter_payload_recu(type_transaction, data):
    """
    Analyse le type de transaction reçu par le réseau et appelle la bonne méthode CRUD.
    """
    if type_transaction == "sauveteur_update":
        # Exemple de gestion de l'update
        sauveteur_crud = SauveteurCRUD()
        
        # Le payload peut contenir des clés que le CRUD n'attend pas
        id_sauveteur = data.get('id')
        nouveau_statut = data.get('statut')
        
        if id_sauveteur and nouveau_statut:
            # Note : Il faudrait idéalement une fonction de 'sync_update' dans le CRUD
            # qui met à jour toutes les colonnes présentes dans 'data'
            sauveteur_crud.update_statut(id_sauveteur, nouveau_statut)
            print(f"[SYNC] Sauveteur ID {id_sauveteur} mis à jour localement sur statut {nouveau_statut}.")
            
    # Ajoutez des blocs 'elif' pour 'planning_update', 'utilisateur_update', etc.
    # ...