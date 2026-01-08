import socket
import json
import os

# Chemin relatif vers le fichier de configuration (adapté à la structure du projet)
# On remonte de 'gestion_sauveteurs/' vers la racine puis dans 'data/' (ou racine directement selon ta config)
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def charger_ips_machines():
    """Charge la liste des adresses IP des machines du réseau depuis le fichier de configuration.

    Cette fonction lit le fichier JSON `config.json` situé dans le même dossier
    (ou défini par `CONFIG_FILE`) et extrait la liste des IPs.

    Returns:
        list[str]: Une liste contenant les adresses IP (ex: ``['192.168.1.10', '192.168.1.11']``).
        Retourne une liste vide si le fichier est introuvable ou mal formé.
    """
    if not os.path.exists(CONFIG_FILE):
        print(f"[ERREUR] Fichier de configuration introuvable : {CONFIG_FILE}")
        return []

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            # On récupère la clé 'machines' ou 'ips' selon ton JSON
            return config.get('machines', [])
    except json.JSONDecodeError:
        print(f"[ERREUR] Le fichier {CONFIG_FILE} n'est pas un JSON valide.")
        return []
    except Exception as e:
        print(f"[ERREUR] Impossible de lire les IPs : {e}")
        return []

def pair():
    """Établit une connexion TCP avec les autres machines (Handshake).

    Cette fonction parcourt la liste des IPs fournie par :func:`charger_ips_machines`
    et tente de se connecter sur le port par défaut (5000).
    
    Elle permet de vérifier quelles machines sont actuellement en ligne et prêtes
    à recevoir des mises à jour de la base de données.

    Note:
        Le timeout est fixé à 0.5 seconde pour ne pas bloquer l'interface graphique
        si une machine est éteinte.

    Returns:
        list[socket.socket]: La liste des objets `socket` connectés avec succès.
    """
    ips = charger_ips_machines()
    sockets_actifs = []
    port = 5000  # Port par défaut pour l'application

    print(f"[RESEAU] Démarrage du pairing vers {len(ips)} machines...")

    for ip in ips:
        try:
            # Création du socket TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5) # Timeout court
            
            # Tentative de connexion
            resultat = s.connect_ex((ip, port))
            
            if resultat == 0:
                print(f"[RESEAU] Succès : Connecté à {ip}")
                sockets_actifs.append(s)
            else:
                # Si échec, on ferme proprement
                s.close()
                # print(f"[RESEAU] Échec vers {ip} (Code: {resultat})")
                
        except Exception as e:
            print(f"[RESEAU] Erreur lors de la connexion à {ip} : {e}")

    print(f"[RESEAU] Pairing terminé. {len(sockets_actifs)} machines connectées.")
    return sockets_actifs

def envoyer_message(message_json, sockets_cibles=None):
    """Envoie un message JSON à une liste de machines connectées.

    Args:
        message_json (str): La chaîne de caractères au format JSON à envoyer.
        sockets_cibles (list[socket.socket], optional): Une liste de sockets ouverts. 
            Si None, appelle :func:`pair` pour trouver les machines actives.

    Returns:
        int: Le nombre de machines ayant reçu le message avec succès.
    """
    if sockets_cibles is None:
        sockets_cibles = pair()

    succes = 0
    # On ajoute un saut de ligne car c'est souvent utilisé comme délimiteur en TCP
    data = (message_json + "\n").encode('utf-8')

    for s in sockets_cibles:
        try:
            s.sendall(data)
            succes += 1
        except Exception as e:
            print(f"[RESEAU] Erreur d'envoi : {e}")
            try:
                s.close()
            except:
                pass
    
    return succes