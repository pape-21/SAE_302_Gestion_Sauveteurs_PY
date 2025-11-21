# Fichier : tests/test_serialisation.py
import sys
import os

# Solution pour l'import si tu n'as pas reconfiguré le terminal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gestion_sauveteurs.utils.serialiseur import creer_payload_update, analyser_payload
import json

def main():
    print("--- Test Serialiseur JSON (Contrat Réseau) ---")
    
    # 1. Préparation des données d'une mise à jour (Backend -> Réseau)
    donnees_a_envoyer = {
        "id": 101,
        "nom": "Dupont",
        "statut": "brancardage civière",
        "departement": "38"
    }
    
    # 2. Sérialisation (Création du message pour Perceval)
    json_payload = creer_payload_update("sauveteur", donnees_a_envoyer)
    
    print("\n1. Payload JSON généré (À ENVOYER) :")
    # Affiche le JSON formaté pour la lisibilité
    print(json.dumps(json.loads(json_payload), indent=2)) 

    # 3. Désérialisation (Simulation de la réception par un autre PC)
    type_recu, data_recue = analyser_payload(json_payload)
    
    print("\n2. Analyse du Payload reçu (À TRAITER) :")
    if type_recu and data_recue:
        print(f"   [OK] Type de transaction : {type_recu}")
        print(f"   [OK] Données reçues : {data_recue}")
        print("   -> L'ID 101 doit passer au statut 'brancardage civière' dans la BDD locale.")
    else:
        print("   [ERREUR] Le format JSON n'a pas pu être analysé correctement.")
    
    print("\n--- Fin du test de sérialisation ---")

if __name__ == "__main__":
    main()