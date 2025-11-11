import socket, json, threading
from  import appliquer_mise_a_jour  # fonction qui applique une mise à jour dans la base

# port de communication entre les machines

PORT = 5002
  
def demarrer_serveur():
    """Serveur TCP qui écoute les autres machines et applique leurs mises à jour"""
    
    def gerer_client(connexion, adresse):
        """Traite une connexion entrante et applique la mise à jour"""
        donnees_recue = b""
        # lire les données jusqu'à la fin de la connexion
        while True:
            fragment = connexion.recv(4096)
            if not fragment:
                break
            donnees_recue += fragment
        if not donnees_recue:
            connexion.close()
            return
        
        mise_a_jour = json.loads(donnees_recue.decode())
        print(f" {adresse} : {mise_a_jour}")
        
        # appliquer la mise à jour dans la base locale
        appliquer_mise_a_jour(mise_a_jour)
        connexion.close()

    # création du serveur TCP
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serveur.bind(("", PORT))  # écouter sur toutes les interfaces réseau
    serveur.listen()
    print(f" Serveur en écoute sur le port {PORT}")

    # boucle principale pour accepter les connexions entrantes
    while True:
        connexion, adresse = serveur.accept()
        threading.Thread(target=gerer_client, args=(connexion, adresse), daemon=True).start()


def envoyer_mise_a_jour(mise_a_jour):
    """Envoie une mise à jour aux autres machines du LAN"""
    
    # lecture du fichier de configuration pour connaître les pairs
    fichier_config = open("config.json")
    configuration = json.load(fichier_config)
    fichier_config.close()

    for ip_pair in configuration.get("peers", []):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(3)
        client.connect((ip_pair, PORT))
        donnees_a_envoyer = json.dumps(mise_a_jour).encode()
        client.sendall(donnees_a_envoyer)
        client.close()
        print(f" {ip_pair}")
