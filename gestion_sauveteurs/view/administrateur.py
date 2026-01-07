import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView,
    QTableWidgetItem, QStackedWidget, QFrame, QLineEdit, QFormLayout
)
from PyQt5.QtCore import Qt

# ================== FENÊTRE AJOUTER UTILISATEUR ==================
class FenetreAjouterUtilisateur(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter Utilisateurs")
        self.setFixedSize(350, 250)
        self.setStyleSheet("background-color: #e9e4de;")

        layout = QVBoxLayout(self)
        bandeau = QLabel("Ajouter Utilisateurs")
        bandeau.setFixedHeight(30)
        bandeau.setAlignment(Qt.AlignCenter)
        bandeau.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold;")
        layout.addWidget(bandeau)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.addRow("nom :", QLineEdit())
        form_layout.addRow("prénom :", QLineEdit())
        form_layout.addRow("profil :", QLineEdit())
        layout.addLayout(form_layout)

        btn = QPushButton("Ajouter")
        btn.setStyleSheet("background-color: #f8f8f8; border: 1px solid gray; padding: 5px;")
        layout.addWidget(btn)

# ================== FENÊTRE SUPPRIMER UTILISATEUR ==================
class FenetreSupprimerUtilisateur(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supprimer Utilisateurs")
        self.setFixedSize(300, 160)
        self.setStyleSheet("background-color: #e9e4de;")

        layout = QVBoxLayout(self)
        bandeau = QLabel("Supprimer Utilisateurs")
        bandeau.setFixedHeight(30)
        bandeau.setAlignment(Qt.AlignCenter)
        bandeau.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold;")
        layout.addWidget(bandeau)

        form_layout = QFormLayout()
        form_layout.addRow("id :", QLineEdit())
        layout.addLayout(form_layout)

        btn = QPushButton("Supprimer")
        btn.setStyleSheet("background-color: #f8f8f8; border: 1px solid gray;")
        layout.addWidget(btn)

# ================== INTERFACE ADMIN ==================
class InterfaceAdmin(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: #e9e4de;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        bandeau = QLabel("Administrateur")
        bandeau.setFixedHeight(45)
        bandeau.setAlignment(Qt.AlignCenter)
        bandeau.setStyleSheet("background-color: #1a6f91; color: white; font-size: 16px; font-weight: bold;")
        main_layout.addWidget(bandeau)

        zone = QHBoxLayout()
        zone.setContentsMargins(20, 20, 20, 20)
        zone.setSpacing(40)

        # Menu latéral
        menu = QVBoxLayout()
        style_btn = "QPushButton { background-color: #f8f8f8; border: 1px solid #b0b0b0; border-radius: 4px; padding: 10px; min-width: 200px; }"

        self.btn_users = QPushButton("modifier les utilisateurs")
        self.btn_infos = QPushButton("informations générales")
        self.btn_plan = QPushButton("voir le planning")

        for b in [self.btn_users, self.btn_infos, self.btn_plan]:
            b.setStyleSheet(style_btn)
            menu.addWidget(b)
        menu.addStretch()

        self.stack = QStackedWidget()

        # --- PAGE 0 : ACCUEIL (Tableau en haut avec 1 ligne de données) ---
        page_accueil = QWidget()
        v1 = QVBoxLayout(page_accueil)
        v1.setContentsMargins(0, 0, 0, 0)
        
        # On ne crée que 1 ligne de données (+ l'en-tête)
        self.table_accueil = self.creer_tableau(["ID", "Nom", "Prenom", "Profil"], 600, 85)
        self.table_accueil.setItem(0, 0, QTableWidgetItem("1"))
        self.table_accueil.setItem(0, 1, QTableWidgetItem("Gueye"))
        self.table_accueil.setItem(0, 2, QTableWidgetItem("Sokhna"))
        self.table_accueil.setItem(0, 3, QTableWidgetItem("admin"))
        
        v1.addWidget(self.table_accueil, alignment=Qt.AlignTop)
        v1.addStretch() # Force le tableau à rester tout en haut

        # --- PAGE 1 : MODIFIER ---
        page_users = QWidget()
        v2 = QVBoxLayout(page_users)
        cadre_u = self.creer_cadre_avec_croix("Utilisateurs", 350, 200)
        lay_u = QVBoxLayout(cadre_u)
        lay_u.setContentsMargins(20, 50, 20, 20)
        self.btn_add = QPushButton("Ajouter utilisateur")
        self.btn_sup = QPushButton("Supprimer utilisateur")
        for b in [self.btn_add, self.btn_sup]:
            b.setStyleSheet(style_btn)
            lay_u.addWidget(b)
        v2.addWidget(cadre_u, alignment=Qt.AlignTop)

        # --- PAGE 2 : INFOS GÉNÉRALES ---
        page_infos = QWidget()
        v3 = QVBoxLayout(page_infos)
        cadre_i = self.creer_cadre_avec_croix("Infos Générales", 620, 150)
        lay_i = QVBoxLayout(cadre_i)
        lay_i.setContentsMargins(10, 50, 10, 10)
        # Tableau infos avec une seule ligne aussi
        lay_i.addWidget(self.creer_tableau(["Nom", "Prenom", "Spécialité", "Département"], 600, 85))
        v3.addWidget(cadre_i, alignment=Qt.AlignTop)
        v3.addStretch()

        self.stack.addWidget(page_accueil)
        self.stack.addWidget(page_users)
        self.stack.addWidget(page_infos)

        zone.addLayout(menu)
        zone.addWidget(self.stack)
        main_layout.addLayout(zone)

        self.btn_users.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_infos.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_add.clicked.connect(self.ouvrir_ajout)
        self.btn_sup.clicked.connect(self.ouvrir_sup)
        self.btn_plan.clicked.connect(self.parent.afficher_le_planning_externe)

    def creer_tableau(self, titres, largeur, hauteur):
        t = QTableWidget(1, len(titres)) # 1 seule ligne de données
        t.setHorizontalHeaderLabels(titres)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        t.verticalHeader().setVisible(False)
        t.setFixedSize(largeur, hauteur)
        t.setStyleSheet("""
            QTableWidget { 
                background-color: #4b89c5; 
                border: 2px solid #0d3b66; 
                gridline-color: #0d3b66;
                color: black; 
                font-weight: bold; 
            }
        """)
        return t

    def creer_cadre_avec_croix(self, titre, w, h):
        cadre = QFrame()
        cadre.setFixedSize(w, h)
        cadre.setStyleSheet("border: 2px solid #1a6f91; background-color: #e9e4de;")
        bandeau = QLabel(titre, cadre)
        bandeau.setGeometry(0, 0, w, 30)
        bandeau.setAlignment(Qt.AlignCenter)
        bandeau.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold; border: none;")
        btn_x = QPushButton("X", cadre)
        btn_x.setGeometry(w-25, 5, 20, 20)
        btn_x.setStyleSheet("color: white; font-weight: bold; background: transparent; border: none;")
        btn_x.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        return cadre

    def ouvrir_ajout(self):
        self.fen_ajout = FenetreAjouterUtilisateur()
        self.fen_ajout.show()

    def ouvrir_sup(self):
        self.fen_sup = FenetreSupprimerUtilisateur()
        self.fen_sup.show()

# ================== FENÊTRE PRINCIPALE ==================
class Gestionnaire(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAE Planning")
        self.resize(1100, 700)
        self.setCentralWidget(InterfaceAdmin(self))

    def afficher_le_planning_externe(self):
        try:
            from planning_public import InterfacePlanning
            le_planning = InterfacePlanning(self)
            btn_x = QPushButton("X", le_planning)
            btn_x.setGeometry(1060, 5, 30, 30)
            btn_x.setStyleSheet("color: white; font-weight: bold; background: transparent; border: none; font-size: 18px;")
            btn_x.clicked.connect(lambda: self.setCentralWidget(InterfaceAdmin(self)))
            self.setCentralWidget(le_planning)
        except ImportError:
            print("Fichier planning_public.py non trouvé.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Gestionnaire()
    win.show()
    sys.exit(app.exec_())