import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog)
from PyQt5.QtCore import Qt

# Imports  de mon Backend
from gestion_sauveteurs.crud.utilisateur import UtilisateurCRUD

class InterfaceLogin(QWidget):
    """Widget contenant le formulaire de connexion."""
    
    def __init__(self, fenetre_parente=None):
        super().__init__()
        self.fenetre_parente = fenetre_parente
        self.controleur = UtilisateurCRUD()

        self.setStyleSheet("background-color: #e9e4de;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        barre_titre = QLabel("Connexion")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(60)
        barre_titre.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold; font-size: 16px;")
        layout_principal.addWidget(barre_titre)

        layout_principal.addStretch()

        h_user = QHBoxLayout()
        h_user.addStretch()
        h_user.addWidget(QLabel("Identifiant :"))
        self.user = QLineEdit()
        self.user.setFixedWidth(200)
        h_user.addWidget(self.user)
        h_user.addStretch()
        layout_principal.addLayout(h_user)

        h_pw = QHBoxLayout()
        h_pw.addStretch()
        h_pw.addWidget(QLabel("Mot de passe :"))
        self.pw = QLineEdit()
        self.pw.setFixedWidth(200)
        self.pw.setEchoMode(QLineEdit.Password)
        h_pw.addWidget(self.pw)
        h_pw.addStretch()
        layout_principal.addLayout(h_pw)

        layout_principal.addSpacing(20)

        h_btn = QHBoxLayout()
        h_btn.addStretch()
        self.btn_connect = QPushButton("Se connecter")
        self.btn_connect.clicked.connect(self.action_login)
        self.btn_connect.setStyleSheet("padding: 8px 15px; font-weight: bold;")
        h_btn.addWidget(self.btn_connect)
        h_btn.addStretch()
        layout_principal.addLayout(h_btn)

        layout_principal.addStretch()

    def action_login(self):
        """Vérifie les identifiants et ferme la fenêtre en cas de succès."""
        identifiant = self.user.text()
        mdp = self.pw.text()
        
        # Vérification dans la bdd
        role = self.controleur.verifier_connexion(identifiant, mdp)
        
        if role:

            if self.fenetre_parente:
                self.fenetre_parente.role_authentifie = role
                self.fenetre_parente.accept() # Ferme le dialogue avec succès 
        else:
            QMessageBox.warning(self, "Erreur", "Identifiant ou mot de passe incorrect.")


class FenetreLogin(QDialog):
    """Fenêtre de dialogue principale pour le login (bloquante)."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentification - SAE Planning")
        self.resize(500, 300)
        self.role_authentifie = None # Variable pour stocker le résultat
        
        # On intègre le widget créé plus haut                                                                             
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.widget_login = InterfaceLogin(self)
        layout.addWidget(self.widget_login)                            

def lancer_login():

    """Fonction helper pour afficher la fenêtre de login et récupérer le rôle.

    Cette fonction crée une application Qt (si elle n'existe pas), lance
    la fenêtre de connexion en mode modal (bloquant), et attend que l'utilisateur
    se connecte.

    Returns:
        str | None: Le rôle de l'utilisateur ('administrateur', 'gestionnaire'...) 
                    ou None si la fenêtre est fermée sans connexion.
    """
    # On récupère l'instance QApplication existante ou on en crée une
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        
    dialogue = FenetreLogin()
    
    # exec_() lance la boucle locale et bloque le code ici jusqu'à la fermeture
    resultat = dialogue.exec_() 
    
    if resultat == QDialog.Accepted:
        return dialogue.role_authentifie
    else:
        return None

# Pour tester le fichier seul
if __name__ == "__main__":
    role = lancer_login()
    print(f"Rôle récupéré : {role}")