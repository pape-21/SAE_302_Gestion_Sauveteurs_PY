import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
    QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QHeaderView, QFrame
)
from PyQt5.QtCore import Qt

class InterfaceLogin(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: #e9e4de;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # Barre de titre bleue (image_6ae7bf.png)
        barre_titre = QLabel("Application de gestion de planning")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(40)
        barre_titre.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold; border-bottom: 2px solid #004d66;")
        layout_principal.addWidget(barre_titre)

        # Conteneur central
        centre = QWidget()
        layout_centre = QVBoxLayout(centre)
        
        # Bouton Voir le planing en haut à droite
        h_btn_voir = QHBoxLayout()
        h_btn_voir.addStretch()
        self.btn_voir = QPushButton("Voir le planing")
        self.btn_voir.setStyleSheet("background-color: white; border: 1px solid gray; padding: 5px;")
        h_btn_voir.addWidget(self.btn_voir)
        layout_centre.addLayout(h_btn_voir)
        layout_centre.addStretch()

        # Formulaire
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # Ligne Login
        h_login = QHBoxLayout()
        h_login.addStretch()
        h_login.addWidget(QLabel("Login"))
        self.user = QLineEdit()
        self.user.setFixedWidth(200)
        h_login.addWidget(self.user)
        h_login.addStretch()
        form_layout.addLayout(h_login)

        # Ligne Mot de passe
        h_pass = QHBoxLayout()
        h_pass.addStretch()
        h_pass.addWidget(QLabel("Mot de passe"))
        self.pw = QLineEdit()
        self.pw.setFixedWidth(200)
        self.pw.setEchoMode(QLineEdit.Password)
        h_pass.addWidget(self.pw)
        h_pass.addStretch()
        form_layout.addLayout(h_pass)
        
        layout_centre.addWidget(form_widget)
        layout_centre.addSpacing(40)

        # Bouton Se connecter en bas
        h_conn = QHBoxLayout()
        h_conn.addStretch()
        self.btn_connect = QPushButton("Se connecter")
        self.btn_connect.setStyleSheet("background-color: #f0f0f0; border: 1px solid gray; padding: 10px 30px;")
        h_conn.addWidget(self.btn_connect)
        h_conn.addStretch()
        layout_centre.addLayout(h_conn)
        layout_centre.addStretch()

        layout_principal.addWidget(centre)

        # Liaison du bouton "Voir le planing"
        self.btn_voir.clicked.connect(self.parent.afficher_planning)

class InterfacePlanning(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: #e9e4de;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # Barre de titre bleue (image_6ae6eb.png)
        barre_titre = QLabel("Le Planning")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(40)
        barre_titre.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold;")
        layout_principal.addWidget(barre_titre)

        # Zone du tableau
        contenu = QWidget()
        layout_contenu = QVBoxLayout(contenu)
        layout_contenu.setContentsMargins(50, 50, 50, 50)

        self.table = QTableWidget(3, 7)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #4b89c5; gridline-color: #0d3b66; color: black; border: 2px solid #0d3b66; }
            QHeaderView::section { background-color: #4b89c5; border: 1px solid #0d3b66; padding: 4px; }
        """)
        
        # En-têtes (image_6af627.png)
        heures = ["10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30"]
        noms = ["René lapin", "Albert Zorg", "Romain AL"]
        
        self.table.setHorizontalHeaderLabels(heures)
        self.table.setVerticalHeaderLabels(noms)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Exemple "pre" (image_6ae6eb.png)
        item_pre = QTableWidgetItem("pre")
        item_pre.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(1, 2, item_pre)

        layout_contenu.addWidget(self.table)
        
        # Bouton Retour
        self.btn_back = QPushButton("Retour")
        self.btn_back.setFixedWidth(100)
        self.btn_back.clicked.connect(self.parent.afficher_login)
        layout_contenu.addWidget(self.btn_back)

        layout_principal.addWidget(contenu)

class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion Planning")
        self.resize(1000, 600)
        self.afficher_login()

    def afficher_login(self):
        self.setCentralWidget(InterfaceLogin(self))

    def afficher_planning(self):
        self.setCentralWidget(InterfacePlanning(self))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FenetrePrincipale()
    win.show()
    sys.exit(app.exec_())
    