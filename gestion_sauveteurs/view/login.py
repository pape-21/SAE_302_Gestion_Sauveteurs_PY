import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt

# --- IMPORTS DES VUES ET DU BACKEND ---
from gestion_sauveteurs.crud.utilisateur import UtilisateurCRUD
from gestion_sauveteurs.view.planning_public import InterfacePlanning
from gestion_sauveteurs.view.administrateur import FenetreAdministrateur
# On importe la fenêtre qu'on vient de finir (alias pour la clarté)
from gestion_sauveteurs.view.gestionnaire import MainWindow as FenetreGestionnaire

class InterfaceLogin(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.controleur = UtilisateurCRUD()

        # --- STYLE ---
        self.setStyleSheet("background-color: #e9e4de;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # Bandeau
        barre_titre = QLabel("Application de gestion de planning")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(40)
        barre_titre.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold;")
        layout_principal.addWidget(barre_titre)

        # Bouton Planning Public
        h_top = QHBoxLayout()
        h_top.addStretch()
        self.btn_planning = QPushButton("Voir le planing")
        h_top.addWidget(self.btn_planning)
        layout_principal.addLayout(h_top)

        layout_principal.addStretch()

        # Champ Login
        h_user = QHBoxLayout()
        h_user.addStretch()
        h_user.addWidget(QLabel("Login"))
        self.user = QLineEdit()
        self.user.setFixedWidth(200)
        h_user.addWidget(self.user)
        h_user.addStretch()
        layout_principal.addLayout(h_user)

        # Champ Mdp
        h_pw = QHBoxLayout()
        h_pw.addStretch()
        h_pw.addWidget(QLabel("Mot de passe"))
        self.pw = QLineEdit()
        self.pw.setFixedWidth(200)
        self.pw.setEchoMode(QLineEdit.Password)
        h_pw.addWidget(self.pw)
        h_pw.addStretch()
        layout_principal.addLayout(h_pw)

        layout_principal.addSpacing(20)

        # Bouton Connecter
        h_btn = QHBoxLayout()
        h_btn.addStretch()
        self.btn_connect = QPushButton("Se connecter")
        h_btn.addWidget(self.btn_connect)
        h_btn.addStretch()
        layout_principal.addLayout(h_btn)

        layout_principal.addStretch()

        # Connexions
        self.btn_planning.clicked.connect(self.action_voir_planning)
        self.btn_connect.clicked.connect(self.action_login)

    def action_voir_planning(self):
        self.fenetre_pub = InterfacePlanning()
        self.fenetre_pub.show()

    def action_login(self):
        identifiant = self.user.text()
        mdp = self.pw.text()
        
        # Le CRUD renvoie : 'administrateur', 'gestionnaire', ou None
        role = self.controleur.verifier_connexion(identifiant, mdp)
        
        if role:
            # --- C'EST ICI QUE SE FAIT L'AIGUILLAGE ---
            if self.parent:
                if role == 'administrateur':
                    self.parent.afficher_admin()
                elif role == 'gestionnaire':
                    self.parent.afficher_gestionnaire()
                elif role == 'lecture':
                    # Si tu as un utilisateur "lecture seule", on peut renvoyer vers le planning public
                    self.action_voir_planning()
                else:
                    QMessageBox.warning(self, "Erreur", f"Rôle inconnu : {role}")
        else:
            QMessageBox.warning(self, "Erreur", "Identifiants incorrects")


# Classe principale (Conteneur)
class Gestionnaire(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAE Planning")
        self.resize(1000, 600)
        self.afficher_login()

    def afficher_login(self):
        """Affiche l'écran de connexion."""
        self.setCentralWidget(InterfaceLogin(self))

    def afficher_admin(self):
        """Affiche l'écran Administrateur."""
        self.setCentralWidget(FenetreAdministrateur())

    def afficher_gestionnaire(self):
        """Affiche l'écran Gestionnaire."""
        self.setCentralWidget(FenetreGestionnaire())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Gestionnaire()
    win.show()
    sys.exit(app.exec_())