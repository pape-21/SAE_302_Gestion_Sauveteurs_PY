import socket
import threading
import json

class RéseauPairÀPair:
    """
    Réseau peer-to-peer basique.
    Écoute sur un port donné et échange des mises à jour JSON entre machines.
    """

    def __init__(self, liste_machines, port=5002, fonction_mise_a_jour=None, ip_locale=None):
        # Liste des machines du réseau
        self.machines = liste_machines or []
        if ip_locale in self.machines:
            self.machines.remove(ip_locale)

        self.port = port
        self.fonction_mise_a_jour = fonction_mise_a_jour
        self.stop_event = threading.Event()

        # Lancer le serveur d’écoute
        threading.Thread(target=self._serveur, daemon=True).start()
        print(f"[Réseau] Serveur P2P démarré sur le port {self.port}")

    # ------------------------------------------------------------------
    # SERVEUR : écoute les connexions entrantes
    # ------------------------------------------------------------------
    def _serveur(self):
        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind(('', self.port))
        serveur.listen()

        while not self.stop_event.is_set():
            try:
                serveur.settimeout(1)
                client, adresse = serveur.accept()
                threading.Thread(target=self._gerer_client, args=(client,), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[Réseau] Erreur serveur : {e}")

        serveur.close()
        print("[Réseau] Serveur arrêté")

    # ------------------------------------------------------------------
    # CLIENT : reçoit un message d’un autre poste
    # ------------------------------------------------------------------
    def _gerer_client(self, client):
        with client:
            try:
                donnees = client.recv(65536)
                if not donnees:
                    return

                message = json.loads(donnees.decode('utf-8'))

                # Appeler la fonction de mise à jour
                if self.fonction_mise_a_jour:
                    self.fonction_mise_a_jour(message)

            except Exception as e:
                print(f"[Réseau] Erreur client : {e}")

    # ------------------------------------------------------------------
    # ENVOI : diffuse une mise à jour à tous les pairs
    # ------------------------------------------------------------------
    def diffuser_mise_a_jour(self, mise_a_jour):
        donnees = json.dumps(mise_a_jour).encode('utf-8')

        for ip in self.machines:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((ip, self.port))
                sock.sendall(donnees)
                sock.close()
            except Exception as e:
                print(f"[Réseau] Impossible de contacter {ip} : {e}")

    # ------------------------------------------------------------------
    # ARRÊT DU SERVEUR
    # ------------------------------------------------------------------
    def arreter(self):
        self.stop_event.set()
