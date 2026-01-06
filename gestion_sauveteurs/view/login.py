import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from planning_public import InterfacePlanning

class InterfaceLogin(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: #e9e4de;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        barre_titre = QLabel("Application de gestion de planning")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(40)
        barre_titre.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold;")
        layout_principal.addWidget(barre_titre)

        h_top = QHBoxLayout()
        h_top.addStretch()
        self.btn_planning = QPushButton("Voir le planing")
        h_top.addWidget(self.btn_planning)
        layout_principal.addLayout(h_top)

        layout_principal.addStretch()

        h_user = QHBoxLayout()
        h_user.addStretch()
        h_user.addWidget(QLabel("Login"))
        self.user = QLineEdit()
        self.user.setFixedWidth(200)
        h_user.addWidget(self.user)
        h_user.addStretch()
        layout_principal.addLayout(h_user)

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

        h_btn = QHBoxLayout()
        h_btn.addStretch()
        self.btn_connect = QPushButton("Se connecter")
        h_btn.addWidget(self.btn_connect)
        h_btn.addStretch()
        layout_principal.addLayout(h_btn)

        layout_principal.addStretch()

        self.btn_planning.clicked.connect(self.parent.afficher_le_planning_externe)

class Gestionnaire(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAE Planning")
        self.resize(1000, 600)
        self.afficher_login()

    def afficher_login(self):
        self.setCentralWidget(InterfaceLogin(self))

    def afficher_le_planning_externe(self):
        self.setCentralWidget(InterfacePlanning(self))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Gestionnaire()
    win.show()
    sys.exit(app.exec_())