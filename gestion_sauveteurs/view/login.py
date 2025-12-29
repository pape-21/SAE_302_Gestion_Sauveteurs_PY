import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class FenetreLogin(QWidget):
    def __init__(self, fonction_connexion=None, fonction_voir_planning=None):
        super().__init__()
        # Ces fonctions seront fournies par le contrôleur (Toi) plus tard
        self.fonction_connexion = fonction_connexion
        self.fonction_voir_planning = fonction_voir_planning
        
        self.configurer_fenetre()
        self.creer_interface()

    def configurer_fenetre(self):
        self.setWindowTitle("Application de gestion de planning")
        self.resize(700, 450)

    def creer_interface(self):
        # Layout principal vertical
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(0)

        # --- 1. Bandeau Supérieur ---
        label_titre = QLabel("Application de gestion de planning")
        label_titre.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(label_titre)

        # --- 2. Zone de Contenu ---
        widget_contenu = QWidget()
        layout_contenu = QVBoxLayout()
        widget_contenu.setLayout(layout_contenu)

        # Bouton "Voir le planning" aligné à droite
        layout_bouton_haut = QHBoxLayout()
        layout_bouton_haut.addStretch()
        
        self.bouton_planning = QPushButton("Voir le planning")
        
        if self.fonction_voir_planning:
            self.bouton_planning.clicked.connect(self.fonction_voir_planning)
            
        layout_bouton_haut.addWidget(self.bouton_planning)
        layout_bouton_haut.addSpacing(20) # Marge à droite
        layout_contenu.addLayout(layout_bouton_haut)

        # Formulaire de connexion
        layout_formulaire = QFormLayout()
        layout_formulaire.setLabelAlignment(Qt.AlignRight)
        layout_formulaire.setVerticalSpacing(15)

        # Champ Login
        label_login = QLabel("Login")
        label_login.setFont(QFont("Arial", 10))
        self.champ_login = QLineEdit()
        self.champ_login.setFixedWidth(200)
        
        # Champ Mot de passe
        label_mdp = QLabel("Mot de passe")
        label_mdp.setFont(QFont("Arial", 10))
        self.champ_mdp = QLineEdit()
        self.champ_mdp.setEchoMode(QLineEdit.Password)
        self.champ_mdp.setFixedWidth(200)

        layout_formulaire.addRow(label_login, self.champ_login)
        layout_formulaire.addRow(label_mdp, self.champ_mdp)

        # Centrage du formulaire
        widget_form = QWidget()
        widget_form.setLayout(layout_formulaire)
        layout_centre = QHBoxLayout()
        layout_centre.addStretch()
        layout_centre.addWidget(widget_form)
        layout_centre.addStretch()
        layout_contenu.addLayout(layout_centre)

        layout_contenu.addSpacing(20)

        # Bouton "Se connecter"
        layout_bouton_bas = QHBoxLayout()
        layout_bouton_bas.addStretch()
        
        self.bouton_connecter = QPushButton("Se connecter")
        self.bouton_connecter.setCursor(Qt.PointingHandCursor)
        self.bouton_connecter.setFixedWidth(150)
        
        
        self.bouton_connecter.clicked.connect(self.action_connecter)
        
        layout_bouton_bas.addWidget(self.bouton_connecter)
        layout_bouton_bas.addStretch()
        layout_contenu.addLayout(layout_bouton_bas)

        layout_contenu.addStretch() # Espace vide en bas

        layout_principal.addWidget(widget_contenu)
        self.setLayout(layout_principal)

    def action_connecter(self):
        login = self.champ_login.text()
        mdp = self.champ_mdp.text()
        if self.fonction_connexion:
            self.fonction_connexion(login, mdp)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetreLogin()
    fenetre.show()
    sys.exit(app.exec_())