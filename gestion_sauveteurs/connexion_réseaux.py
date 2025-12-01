import socket
import threading
import json
import os  # Nécessaire pour trouver le fichier config

def charger_ips_machines():
    """
    Lit le fichier config.json situé dans le même dossier 
    et retourne la liste des adresses IP des pairs.
    """
    chemin_config = os.path.join(os.path.dirname(__file__), 'config.json')
    
    # Si le fichier n'existe pas, on retourne une liste vide
    if not os.path.exists(chemin_config):
        print(f"[CONFIG] Fichier introuvable : {chemin_config}")
        return []

    try:
        with open(chemin_config, 'r') as f:
            config = json.load(f)
            # On récupère la liste sous la clé "pairs" (ou "machines" par sécurité)
            return config.get("pairs", config.get("machines", []))
    except Exception as e:
        print(f"[CONFIG] Erreur de lecture : {e}")
        return []

class pair:
    
    """
    Réseau peer-to-peer basique.
    Écoute sur un port donné et échange des mises à jour JSON entre machines.
    """

    def __init__(self, liste_machines, port=5002, fonction_mise_a_jour=None, ip_locale=None):
        # Liste des machines du réseau
        self.machines = liste_machines or []
        
        # On évite de s'envoyer des messages à soi-même si l'IP locale est dans la liste
        if ip_locale in self.machines:
            self.machines.remove(ip_locale)

        self.port = port
        self.fonction_mise_a_jour = fonction_mise_a_jour
        self.stop_event = threading.Event()

        # Lancer le serveur d’écoute
        threading.Thread(target=self._serveur, daemon=True).start()
        print(f"[RESEAU] Serveur P2P démarré sur le port {self.port}")

    # SERVEUR : écoute les connexions entrantes
    def _serveur(self):
        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # On écoute sur toutes les interfaces
        try:
            serveur.bind(('0.0.0.0', self.port))
        except Exception as e:
            print(f"[ERREUR RESEAU] Impossible de lier le port {self.port}: {e}")
            return

        serveur.listen()

        while not self.stop_event.is_set():
            try:
                serveur.settimeout(1)
                client, adresse = serveur.accept()
                threading.Thread(target=self._gerer_client, args=(client,), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[RESEAU] Erreur serveur : {e}")

        serveur.close()
        print("[RESEAU] Serveur arrêté")

    # CLIENT (RECEPTION) : reçoit un message d’un autre poste
    def _gerer_client(self, client):
        with client:
            try:
                donnees = client.recv(65536)
                if not donnees:
                    return

                message = json.loads(donnees.decode('utf-8'))

                # Appeler la fonction de mise à jour du contrôleur
                if self.fonction_mise_a_jour:
                    # On passe aussi l'adresse de l'expéditeur pour info
                    adresse_expediteur = client.getpeername()[0]
                    self.fonction_mise_a_jour(message, adresse_expediteur)

            except Exception as e:
                print(f"[RESEAU] Erreur lors de la réception : {e}")

    # ENVOI : diffuse une mise à jour à tous les pairs
    def diffuser_mise_a_jour(self, mise_a_jour):
        donnees = json.dumps(mise_a_jour).encode('utf-8')

        for ip in self.machines:
            try:
                print(f"Envoi vers {ip}...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((ip, self.port))
                sock.sendall(donnees)
                sock.close()
            except Exception as e:
                print(f"[RESEAU] Échec envoi vers {ip} : {e}")

    # ARRÊT DU SERVEUR
    def arreter(self):
        self.stop_event.set()