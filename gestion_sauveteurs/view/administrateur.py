import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QHeaderView, QDialog, QLineEdit, QFormLayout, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DialogueAjoutUtilisateur(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter Utilisateurs")
        self.setFixedSize(300, 250)
        
        # Titre
        lbl_titre = QLabel("Ajouter Utilisateurs", self)
        lbl_titre.setAlignment(Qt.AlignCenter)
        lbl_titre.setGeometry(0, 0, 300, 30)

        layout = QFormLayout()
        layout.setContentsMargins(20, 50, 20, 20)
        
        self.champ_nom = QLineEdit()
        self.champ_prenom = QLineEdit()
        self.combo_profil = QComboBox()
        self.combo_profil.addItems(["administrateur", "gestionnaire", "lecture"])
        self.champ_mdp = QLineEdit() 
        self.champ_mdp.setPlaceholderText("Mot de passe")

        layout.addRow("Nom :", self.champ_nom)
        layout.addRow("Prénom :", self.champ_prenom)
        layout.addRow("Profil :", self.combo_profil)
        layout.addRow("Mdp :", self.champ_mdp)

        self.btn_ajouter = QPushButton("Ajouter")
        self.btn_ajouter.setFixedWidth(100)
        layout.addRow("", self.btn_ajouter) 
        
        self.setLayout(layout)

# --- SOUS-FENÊTRE : Supprimer Utilisateur ---
class DialogueSupprimerUtilisateur(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Supprimer Utilisateurs")
        self.setFixedSize(300, 150)

        lbl_titre = QLabel("Supprimer Utilisateurs", self)
        lbl_titre.setAlignment(Qt.AlignCenter)
        lbl_titre.setGeometry(0, 0, 300, 30)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 20)
        
        layout_h = QHBoxLayout()
        layout_h.addWidget(QLabel("id :"))
        self.champ_id = QLineEdit()
        layout_h.addWidget(self.champ_id)
        layout.addLayout(layout_h)

        self.btn_supprimer = QPushButton("Supprimer")
        layout.addWidget(self.btn_supprimer, alignment=Qt.AlignCenter)
        self.setLayout(layout)

# --- FENÊTRE PRINCIPALE : ADMINISTRATEUR ---
class FenetreAdministrateur(QWidget):
    def __init__(self):
        super().__init__()
        self.configurer_fenetre()
        self.creer_interface()

    def configurer_fenetre(self):
        self.setWindowTitle("Espace Administrateur")
        self.resize(900, 500)

    def creer_interface(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # 1. Bandeau
        label_titre = QLabel("Administrateur")
        label_titre.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(label_titre)

        # 2. Zone centrale (Boutons à gauche, Tableau à droite)
        layout_centre = QHBoxLayout()
        layout_centre.setContentsMargins(20, 20, 20, 20)

        # --- Colonne Gauche : Boutons ---
        layout_boutons = QVBoxLayout()
        layout_boutons.setAlignment(Qt.AlignTop)
        layout_boutons.setSpacing(15)

        self.btn_modifier_users = QPushButton("Modifier les utilisateurs")
        self.btn_modifier_users.clicked.connect(self.ouvrir_dialogue_ajout) 

        self.btn_infos_generales = QPushButton("Informations générales")

        self.btn_voir_planning = QPushButton("Voir le planning")

        layout_boutons.addWidget(self.btn_modifier_users)
        layout_boutons.addWidget(self.btn_infos_generales)
        layout_boutons.addWidget(self.btn_voir_planning)
        layout_boutons.addStretch() 

        # --- Colonne Droite : Tableau ---
        self.tableau_users = QTableWidget()
        self.tableau_users.setColumnCount(4)
        self.tableau_users.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Profil"])
        self.tableau_users.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout_centre.addLayout(layout_boutons, 1) 
        layout_centre.addWidget(self.tableau_users, 3) 

        layout_principal.addLayout(layout_centre)
        self.setLayout(layout_principal)

    # --- Méthodes pour ouvrir les sous-fenêtres ---
    def ouvrir_dialogue_ajout(self):
        dial = DialogueAjoutUtilisateur(self)
        dial.exec_()

    def ouvrir_dialogue_suppression(self):
        dial = DialogueSupprimerUtilisateur(self)
        dial.exec_()

# --- Bloc de test 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fen = FenetreAdministrateur()
    fen.show()
    sys.exit(app.exec_())