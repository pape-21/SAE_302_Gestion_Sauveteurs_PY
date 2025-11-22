
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import threading

from gestion_sauveteurs.resaux import GestionnaireReseau
from gestion_sauveteurs.utils.serialiseur import creer_payload_update, analyser_payload


messages_recus = []
def traiter_payload_recu_mock(type_transaction, donnees):
    print(f"Reçu: {type_transaction} - Données: {donnees['statut']}")
    messages_recus.append(donnees)


def main():
    print("Test Gestionnaire Réseau P2P")

    gestionnaire_reseau = GestionnaireReseau(traiter_payload_recu_mock)
    
    # Démarrage de l'écoute
    gestionnaire_reseau.demarrer_ecoute()
    time.sleep(1) 

    donnees_maj = {
        "id": 1,
        "nom": "Perceval",
        "statut": "sous_terre"
    }
    payload_json = creer_payload_update("sauveteur", donnees_maj)

    
    print("Envoi de la mise à jour")
    gestionnaire_reseau.envoyer_maj_a_un_client(payload_json)
    
    time.sleep(2) 

    print("Vérification des résultats")
    if len(messages_recus) == 1 and messages_recus[0]['statut'] == 'sous_terre':
        print("Le message a été envoyé et reçu correctement par le thread serveur.")
    else:
        print("Échec de la communication réseau simulée.")

    gestionnaire_reseau.arreter()
    print("Fin du test")

if __name__ == "__main__":
    main()