# Fichier : gestion_sauveteurs/utils/serialiseur.py
import json
from datetime import datetime

# --- Définition du Contrat (Basé sur ton accord avec Perceval) ---
# Format pour une mise à jour réseau (update)

def creer_payload_update(type_entite, data_dict):
    """
    Crée la structure JSON complète pour l'envoi d'une modification unique.

    type_entite : 'sauveteur', 'utilisateur', 'planning'
    data_dict : le dictionnaire de la ligne modifiée (ex: {'id': 5, 'statut': 'sous_terre'})
    """
    payload = {
        "type": f"{type_entite}_update",
        "timestamp": datetime.now().isoformat(),
        "data": data_dict
    }
    return json.dumps(payload)

def analyser_payload(json_string):
    """
    Prend une chaîne JSON reçue et retourne son type et son dictionnaire de données.
    """
    try:
        payload = json.loads(json_string)
        
        # Vérification du format
        if 'type' in payload and 'data' in payload:
            return payload['type'], payload['data']
        else:
            print("[ERREUR] Format de payload incomplet.")
            return None, None
            
    except json.JSONDecodeError as e:
        print(f"[ERREUR] Impossible de décoder le JSON : {e}")
        return None, None