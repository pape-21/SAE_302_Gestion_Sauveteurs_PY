import socket
import json
import os
import threading
import time

# --- MODIFICATION : Retour vers config.json ---
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def charger_config():
    """Charge la configuration complète (port et machines) depuis config.json."""
    # Valeurs par défaut
    default_config = {"port": 5002, "machines": []}
    
    if not os.path.exists(CONFIG_FILE):
        return default_config
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return default_config

class ServeurThread(threading.Thread):
    """Thread qui écoute les connexions entrantes (Mode Serveur)."""
    def __init__(self, port, callback_mise_a_jour):
        super().__init__()
        self.port = port
        self.callback = callback_mise_a_jour
        self.running = True

    def run(self):
        print(f"[SERVEUR] Démarrage de l'écoute sur le port {self.port}...")
        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            serveur.bind(('0.0.0.0', self.port))
            serveur.listen(5)
            while self.running:
                conn, addr = serveur.accept()
                threading.Thread(target=self.gerer_client, args=(conn, addr)).start()
        except Exception as e:
            print(f"[SERVEUR] Erreur: {e}")
        finally:
            serveur.close()

    def gerer_client(self, conn, addr):
        """Reçoit les données d'un client connecté."""
        try:
            buffer = ""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                
                # Décodage et gestion des messages collés
                buffer += data.decode('utf-8')
                
                while "\n" in buffer:
                    message_str, buffer = buffer.split("\n", 1)
                    if not message_str.strip():
                        continue
                        
                    print(f"[RECU] De {addr[0]}: {message_str}")
                    
                    try:
                        message_json = json.loads(message_str)
                        if self.callback:
                            self.callback(message_json, addr[0])
                    except json.JSONDecodeError:
                        print(f"[ERREUR] JSON invalide reçu de {addr}")

        except Exception as e:
            print(f"[CONNEXION] Erreur avec {addr}: {e}")
        finally:
            conn.close()

def pair(callback_mise_a_jour=None):
    """
    1. Lit config.json pour trouver le port et les IPs.
    2. Lance le serveur.
    3. Connecte les clients.
    """
    config = charger_config()
    # On utilise le port du fichier, ou 5002 par défaut
    port = config.get("port", 5002)
    ips = config.get("machines", [])

    # 1. SERVEUR
    if callback_mise_a_jour:
        thread_serveur = ServeurThread(port, callback_mise_a_jour)
        thread_serveur.daemon = True 
        thread_serveur.start()

    # 2. CLIENT
    sockets_actifs = []
    print(f"[CLIENT] Tentative de connexion vers {len(ips)} machines sur le port {port}...")
    
    for ip in ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2) 
            if s.connect_ex((ip, port)) == 0:
                print(f"[CLIENT] Connecté à {ip}")
                sockets_actifs.append(s)
            else:
                s.close()
        except:
            pass
            
    return sockets_actifs

def envoyer_message(message_dict, sockets_cibles):
    """Envoie un message JSON avec un saut de ligne."""
    if not sockets_cibles:
        print("[ENVOI] Aucun destinataire connecté.")
        return

    data_json = json.dumps(message_dict) + "\n"
    data_bytes = data_json.encode('utf-8')

    for s in sockets_cibles:
        try:
            s.sendall(data_bytes)
            try:
                ip_dest = s.getpeername()[0]
            except:
                ip_dest = "Inconnu"
            print(f"[ENVOI] Message envoyé à {ip_dest}")
        except Exception as e:
            print(f"[ENVOI] Erreur vers {s}: {e}")