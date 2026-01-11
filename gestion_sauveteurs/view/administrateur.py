import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QHeaderView, QDialog, QLineEdit, QFormLayout, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from gestion_sauveteurs.crud.utilisateur import UtilisateurCRUD

# --- SOUS-FENÊTRE : Ajouter Utilisateur ---
class DialogueAjoutUtilisateur(QDialog):
    """Fenêtre de dialogue pour l'ajout d'un nouvel utilisateur."""

    def __init__(self, parent=None):
        """Initialise le formulaire d'ajout."""
        super().__init__(parent)
        self.setWindowTitle("Ajouter un utilisateur")
        self.setFixedSize(300, 250)
        self.controleur = UtilisateurCRUD() # Connexion au moteur
        
        # Titre
        lbl_titre = QLabel("Nouvel Utilisateur", self)
        lbl_titre.setAlignment(Qt.AlignCenter)
        lbl_titre.setStyleSheet("background-color: #0b66c3; color: white; font-weight: bold; padding: 5px;")
        lbl_titre.setGeometry(0, 0, 300, 30)

        layout = QFormLayout()
        layout.setContentsMargins(20, 50, 20, 20)
        
        # Champs
        self.champ_identifiant = QLineEdit()
        
        self.champ_mdp = QLineEdit() 
        self.champ_mdp.setEchoMode(QLineEdit.Password)

        self.combo_role = QComboBox()
        self.combo_role.addItems(["administrateur", "gestionnaire", "lecture"])

        layout.addRow("Identifiant :", self.champ_identifiant)
        layout.addRow("Mot de passe :", self.champ_mdp)
        layout.addRow("Rôle :", self.combo_role)

        self.btn_ajouter = QPushButton("Valider")
        self.btn_ajouter.clicked.connect(self.action_ajouter)
        layout.addRow("", self.btn_ajouter)
        
        self.setLayout(layout)

    def action_ajouter(self):
        """Récupère les données saisies et appelle le CRUD pour l'insertion."""
        identifiant = self.champ_identifiant.text()
        mdp = self.champ_mdp.text()
        role = self.combo_role.currentText()

        if identifiant and mdp:
            succes = self.controleur.ajouter_utilisateur(identifiant, mdp, role)
            if succes:
                QMessageBox.information(self, "Succès", f"Utilisateur {identifiant} créé.")
                self.accept() # Ferme la fenêtre
            else:
                QMessageBox.warning(self, "Erreur", "Cet identifiant existe déjà.")
        else:
            QMessageBox.warning(self, "Attention", "Remplissez tous les champs.")

# --- SOUS-FENÊTRE : Supprimer Utilisateur ---
class DialogueSupprimerUtilisateur(QDialog):
    """Fenêtre de dialogue pour la suppression d'un utilisateur."""

    def __init__(self, parent=None):
        """Initialise le formulaire de suppression."""
        super().__init__(parent)
        self.setWindowTitle("Supprimer un utilisateur")
        self.setFixedSize(300, 150)
        self.controleur = UtilisateurCRUD()

        lbl_titre = QLabel("Suppression", self)
        lbl_titre.setAlignment(Qt.AlignCenter)
        lbl_titre.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; padding: 5px;")
        lbl_titre.setGeometry(0, 0, 300, 30)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 20)
        
        layout_h = QHBoxLayout()
        layout_h.addWidget(QLabel("Identifiant à supprimer :"))
        self.champ_id = QLineEdit()
        layout_h.addWidget(self.champ_id)
        layout.addLayout(layout_h)

        self.btn_supprimer = QPushButton("Supprimer définitivement")
        self.btn_supprimer.setStyleSheet("color: red;")
        self.btn_supprimer.clicked.connect(self.action_supprimer)
        layout.addWidget(self.btn_supprimer, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def action_supprimer(self):
        """Vérifie l'identifiant et demande confirmation avant suppression."""
        identifiant = self.champ_id.text()
        if identifiant == "admin":
            QMessageBox.critical(self, "Stop", "Impossible de supprimer le super-admin !")
            return

        if QMessageBox.question(self, "Sûr ?", f"Supprimer {identifiant} ?") == QMessageBox.Yes:
            succes = self.controleur.supprimer(identifiant)
            if succes:
                QMessageBox.information(self, "Fait", "Utilisateur supprimé.")
                self.accept()
            else:
                QMessageBox.warning(self, "Erreur", "Utilisateur introuvable.")

# --- FENÊTRE PRINCIPALE : ADMINISTRATEUR ---
class FenetreAdministrateur(QWidget):
    """Interface principale dédiée à l'administrateur (gestion des comptes)."""

    def __init__(self):
        """Configure la fenêtre et charge les données."""
        super().__init__()
        self.controleur = UtilisateurCRUD() 
        self.configurer_fenetre()
        self.creer_interface()
        self.charger_donnees() 

    def configurer_fenetre(self):
        """Paramètre les propriétés de base de la fenêtre (taille, titre)."""
        self.setWindowTitle("Espace Administrateur - Gestion des Comptes")
        self.resize(900, 500)
        self.setStyleSheet("background-color: #f4f4f9;")

    def creer_interface(self):
        """Construit la disposition graphique (Layouts, Boutons, Tableau)."""
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # 1. Bandeau
        label_titre = QLabel("Administration des Utilisateurs")
        label_titre.setAlignment(Qt.AlignCenter)
        label_titre.setStyleSheet("background-color: #0b66c3; color: white; font-size: 16px; font-weight: bold; padding: 15px;")
        layout_principal.addWidget(label_titre)

        # 2. Zone centrale
        layout_centre = QHBoxLayout()
        layout_centre.setContentsMargins(20, 20, 20, 20)

        # --- Colonne Gauche : Boutons ---
        layout_boutons = QVBoxLayout()
        layout_boutons.setAlignment(Qt.AlignTop)
        layout_boutons.setSpacing(15)

        style_btn = """
            QPushButton {
                background-color: white; border: 1px solid #aaa; 
                border-radius: 4px; padding: 10px; text-align: left;
            }
            QPushButton:hover { background-color: #e0e0e0; }
        """

        self.btn_ajouter = QPushButton("Ajouter un utilisateur")
        self.btn_ajouter.setStyleSheet(style_btn)
        self.btn_ajouter.clicked.connect(self.ouvrir_ajout)

        self.btn_supprimer = QPushButton("Supprimer un utilisateur")
        self.btn_supprimer.setStyleSheet(style_btn)
        self.btn_supprimer.clicked.connect(self.ouvrir_suppression)
        
        self.btn_refresh = QPushButton("Actualiser la liste")
        self.btn_refresh.setStyleSheet(style_btn)
        self.btn_refresh.clicked.connect(self.charger_donnees)

        layout_boutons.addWidget(self.btn_ajouter)
        layout_boutons.addWidget(self.btn_supprimer)
        layout_boutons.addWidget(self.btn_refresh)
        layout_boutons.addStretch()

        # --- Colonne Droite : Tableau ---
        self.tableau_users = QTableWidget()
        colonnes = ["ID", "Identifiant", "Rôle"]
        self.tableau_users.setColumnCount(len(colonnes))
        self.tableau_users.setHorizontalHeaderLabels(colonnes)
        self.tableau_users.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableau_users.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        
        self.tableau_users.horizontalHeader().setStyleSheet("::section{background-color: #0b66c3; color: white;}")

        layout_centre.addLayout(layout_boutons, 1)
        layout_centre.addWidget(self.tableau_users, 3)

        layout_principal.addLayout(layout_centre)
        self.setLayout(layout_principal)

    def charger_donnees(self):
        """Récupère la liste des utilisateurs depuis la BDD et remplit le tableau."""
        try:
            users = self.controleur.get_tous()
            self.tableau_users.setRowCount(0)
            
            for i, user in enumerate(users):
                self.tableau_users.insertRow(i)
                self.tableau_users.setItem(i, 0, QTableWidgetItem(str(user['id'])))
                self.tableau_users.setItem(i, 1, QTableWidgetItem(str(user['identifiant'])))
                self.tableau_users.setItem(i, 2, QTableWidgetItem(str(user['role'])))
        except Exception as e:
            print(f"Erreur chargement : {e}")

    def ouvrir_ajout(self):
        """Ouvre la fenêtre modale d'ajout d'utilisateur."""
        dial = DialogueAjoutUtilisateur(self)
        if dial.exec_(): 
            self.charger_donnees()

    def ouvrir_suppression(self):
        """Ouvre la fenêtre modale de suppression d'utilisateur."""
        dial = DialogueSupprimerUtilisateur(self)
        if dial.exec_():
            self.charger_donnees()

# --- FONCTION PUBLIQUE POUR LE CHEF D'ORCHESTRE ---
def lancer_administrateur():
    """Lance l'interface administrateur de manière bloquante.

    Cette fonction instancie la fenêtre `FenetreAdministrateur`, l'affiche,
    et lance la boucle d'événements Qt.
    """
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        
    fenetre = FenetreAdministrateur()
    fenetre.show()
    
    # On lance la boucle. Le script s'arrêtera ici tant que la fenêtre est ouverte.
    app.exec_()

if __name__ == "__main__":
    lancer_administrateur()