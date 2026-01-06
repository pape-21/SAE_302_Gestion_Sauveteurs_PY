import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView, 
                             QTableWidgetItem, QStackedWidget, QFrame)
from PyQt5.QtCore import Qt

class InterfaceAdmin(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: #e9e4de;") 
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        self.bandeau_haut = QLabel("Administrateur")
        self.bandeau_haut.setFixedHeight(45)
        self.bandeau_haut.setAlignment(Qt.AlignCenter)
        self.bandeau_haut.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold; font-size: 16px;")
        layout_principal.addWidget(self.bandeau_haut)

        zone_centrale = QHBoxLayout()
        zone_centrale.setContentsMargins(20, 40, 20, 20)
        zone_centrale.setSpacing(50)

        layout_boutons = QVBoxLayout()
        layout_boutons.setSpacing(15)
        style_menu = "QPushButton { background-color: #f8f8f8; border: 1px solid #b0b0b0; border-radius: 4px; padding: 10px; min-width: 200px; color: black; }"
        
        self.btn_modif = QPushButton("modifier les utilisateurs")
        self.btn_infos = QPushButton("informations générales")
        self.btn_plan = QPushButton("voir le planning")

        for b in [self.btn_modif, self.btn_infos, self.btn_plan]:
            b.setStyleSheet(style_menu)
            layout_boutons.addWidget(b)
        layout_boutons.addStretch()
        zone_centrale.addLayout(layout_boutons)

        self.pile_contenu = QStackedWidget()
        
        self.page_tableau = QWidget()
        lay_t = QVBoxLayout(self.page_tableau)
        self.table_mini = QTableWidget(2, 4)
        self.table_mini.setHorizontalHeaderLabels(["ID", "Nom", "Prenom", "Profil"])
        self.table_mini.verticalHeader().setVisible(False)
        self.table_mini.setFixedSize(450, 110)
        self.table_mini.setStyleSheet("""
            QTableWidget { background-color: #4b89c5; color: black; font-weight: bold; border: 2px solid #0d3b66; }
            QHeaderView::section { background-color: #4b89c5; border: 1px solid #0d3b66; font-weight: bold; }
        """)
        self.table_mini.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        donnees = ["1", "Gueye", "Sokhna", "admin"]
        for col, txt in enumerate(donnees):
            item = QTableWidgetItem(txt)
            item.setTextAlignment(Qt.AlignCenter)
            self.table_mini.setItem(0, col, item)
        lay_t.addWidget(self.table_mini, alignment=Qt.AlignTop)
        lay_t.addStretch()
        
        self.page_modif = QWidget()
        lay_m = QVBoxLayout(self.page_modif)
        cadre = QFrame()
        cadre.setFixedSize(300, 200)
        cadre.setStyleSheet("border: 2px solid #1a6f91; background-color: #e9e4de;")
        v_lay = QVBoxLayout(cadre)
        v_lay.setContentsMargins(0,0,0,0)
        titre_m = QLabel("Utilisateurs")
        titre_m.setFixedHeight(30)
        titre_m.setAlignment(Qt.AlignCenter)
        titre_m.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold; border: none;")
        v_lay.addWidget(titre_m)
        v_lay.addSpacing(20)
        style_op = "QPushButton { background-color: #f8f8f8; border: 1px solid #b0b0b0; padding: 8px; margin: 0 20px; color: black; }"
        self.btn_ajout = QPushButton("Ajouter utilisateur")
        self.btn_suppr = QPushButton("Supprimer utilisateur")
        self.btn_ajout.setStyleSheet(style_op)
        self.btn_suppr.setStyleSheet(style_op)
        v_lay.addWidget(self.btn_ajout)
        v_lay.addWidget(self.btn_suppr)
        v_lay.addStretch()
        lay_m.addWidget(cadre, alignment=Qt.AlignTop)
        lay_m.addStretch()

        self.pile_contenu.addWidget(self.page_tableau)
        self.pile_contenu.addWidget(self.page_modif)

        zone_centrale.addWidget(self.pile_contenu)
        layout_principal.addLayout(zone_centrale)

        self.btn_plan.clicked.connect(self.parent.afficher_le_planning_externe)
        self.btn_modif.clicked.connect(lambda: self.pile_contenu.setCurrentIndex(1))

if __name__ == "__main__":
    class Simulateur:
        def afficher_le_planning_externe(self): print("Lien planning")
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.resize(1000, 600)
    win.setCentralWidget(InterfaceAdmin(Simulateur()))
    win.show()
    sys.exit(app.exec_())