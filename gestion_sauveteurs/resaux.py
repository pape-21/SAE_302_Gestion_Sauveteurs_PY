
import socket
import threading
import json
import os 

from gestion_sauveteurs.utils.serialiseur import analyser_payload

# Chemin du fichier de configuration, maintenant dans le même dossier
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

class GestionnaireReseau:
    def __init__(self, fonction_maj_bdd):
        self.mise_a_jour_bdd_distante = fonction_maj_bdd
        self.thread_serveur = None
        self.en_cours = False
        
        # --- LOGIQUE DE CONFIGURATION ---
        self.configuration = self._charger_configuration()
        self.PORT = self.configuration.get('port', 5002) 
        self.ADRESSES_PAIRS = self.configuration.get('pairs', [])
        print(f"[RESEAU] Configuration chargée. Port: {self.PORT}. Clients: {len(self.ADRESSES_PAIRS)}")

    def _charger_configuration(self):
        """Lit les adresses des pairs et le port depuis config.json."""
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERREUR CONFIG] Fichier non trouvé à {CONFIG_PATH}. Utilisation des paramètres par défaut.")
            return {'port': 5002, 'pairs': []}
        except json.JSONDecodeError:
            print("[ERREUR CONFIG] Fichier config.json mal formaté.")
            return {'port': 5002, 'pairs': []}

    # --- PARTIE 1 : RÉCEPTION (Serveur TCP) ---
    def demarrer_ecoute(self):
        """Démarre le serveur dans un thread pour écouter les messages entrants."""
        if not self.en_cours:
            self.en_cours = True
            self.thread_serveur = threading.Thread(target=self._executer_serveur)
            self.thread_serveur.daemon = True 
            self.thread_serveur.start()
            print(f"[RESEAU] Serveur en écoute sur le port {self.PORT}...")

    def _executer_serveur(self):
        """Logique d'écoute et de réception des messages."""
        socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        socket_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        
        socket_serveur.bind(('0.0.0.0', self.PORT)) 
        socket_serveur.listen(5)

        while self.en_cours:
            try:
                connexion, adresse = socket_serveur.accept()
                with connexion:
                    message_json_recu = connexion.recv(4096).decode('utf-8')
                    if message_json_recu:
                        type_recu, donnees_recues = analyser_payload(message_json_recu)
                        print(f"[RESEAU] Message reçu de {adresse[0]}. Type: {type_recu}")
                        
                        if type_recu and donnees_recues:
                            self.mise_a_jour_bdd_distante(type_recu, donnees_recues)

            except socket.error as e:
                # Gère l'arrêt propre
                if self.en_cours:
                    print(f"[ERREUR RESEAU] Erreur de connexion serveur : {e}")
                break
        socket_serveur.close()

    # --- PARTIE 2 : ENVOI (Client TCP) ---
    def envoyer_maj_a_un_client(self, payload_json):
        """Envoie la mise à jour à TOUS les clients P2P (incluant 127.0.0.1 pour le test)."""
        for ip_client in self.ADRESSES_PAIRS:
            try:
                socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_client.connect((ip_client, self.PORT))
                
                socket_client.sendall(payload_json.encode('utf-8'))
                print(f"[RESEAU] Payload envoyé avec succès à {ip_client}.")

            except socket.error as e:
                print(f"[ERREUR RESEAU] Échec de l'envoi à {ip_client} : {e}")
            finally:
                socket_client.close()
            
    def arreter(self):
        """Arrête le thread serveur proprement."""
        self.en_cours = False
        try:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('127.0.0.1', self.PORT))
        except socket.error:
            pass