import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QTableWidget, QLineEdit,
    QFormLayout, QStackedWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt5.QtCore import Qt


class InterfacePlanning(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        barre_titre = QLabel("Le Planning")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(40)
        barre_titre.setStyleSheet("""
            background-color: #0b6fa4; 
            color: white; 
            font-weight: bold;
        """)
        layout_principal.addWidget(barre_titre)

        self.table = QTableWidget(3, 7)
        self.table.setStyleSheet("""
            QTableWidget { 
                border: 1px solid #ccc;
            }
            QHeaderView::section { 
                background-color: #0b6fa4; 
                color: white; 
                font-weight: bold;
                padding: 8px;
            }
        """)

        self.table.setHorizontalHeaderLabels(["10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30"])
        self.table.setVerticalHeaderLabels(["René lapin", "Albert Zorg", "Romain AL"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        item = QTableWidgetItem("pre")
        item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(1, 2, item)

        layout_principal.addWidget(self.table)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire")
        self.resize(1000, 600)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # ===== MENU GAUCHE =====
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.setSpacing(5)

        # Titre
        menu_label = QLabel("Gestionnaire")
        menu_label.setAlignment(Qt.AlignCenter)
        menu_label.setFixedHeight(40)
        menu_label.setStyleSheet("""
            background-color: #0b6fa4; 
            color: white; 
            font-weight: bold;
        """)
        menu_layout.addWidget(menu_label)

        # Boutons
        btn_infos = QPushButton("informations générales")
        btn_add_h = QPushButton("ajouter horaire")
        btn_del_h = QPushButton("supprimer horaire")

        btn_infos.clicked.connect(self.show_infos)
        btn_add_h.clicked.connect(self.show_add_horaire)
        btn_del_h.clicked.connect(self.show_del_horaire)

        for btn in [btn_infos, btn_add_h, btn_del_h]:
            btn.setFixedHeight(40)
            menu_layout.addWidget(btn)

        menu_layout.addStretch()

        # ===== ZONE CENTRALE =====
        self.stack = QStackedWidget()

        # Page VIDE au démarrage
        self.page_vide = QWidget()
        self.stack.addWidget(self.page_vide)

        # Page informations générales
        self.page_infos = self.create_infos_page()
        self.stack.addWidget(self.page_infos)

        # Page ajouter horaire
        self.page_add_horaire = self.create_add_horaire_page()
        self.stack.addWidget(self.page_add_horaire)

        # Page supprimer horaire
        self.page_del_horaire = self.create_del_horaire_page()
        self.stack.addWidget(self.page_del_horaire)

        # Page ajouter sauveteur
        self.page_add_sauveteur = self.create_add_sauveteur_page()
        self.stack.addWidget(self.page_add_sauveteur)

        # Page supprimer sauveteur
        self.page_del_sauveteur = self.create_del_sauveteur_page()
        self.stack.addWidget(self.page_del_sauveteur)

        # Afficher page vide au début
        self.stack.setCurrentWidget(self.page_vide)

        # ===== PLANNING =====
        self.planning_widget = InterfacePlanning()

        # ===== ASSEMBLAGE =====
        main_layout.addWidget(menu_widget, 1)
        main_layout.addWidget(self.stack, 2)
        main_layout.addWidget(self.planning_widget, 2)

        self.setCentralWidget(main_widget)

    def create_infos_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(10)

        title = QLabel("informations générales")
        layout.addWidget(title)

        table = QTableWidget(0, 5)
        table.setHorizontalHeaderLabels(["Id", "Nom", "Prenom", "spécialité", "Département"])
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("ajouter sauveteur")
        btn_del = QPushButton("supprimer sauveteur")
        
        btn_add.clicked.connect(self.show_add_sauveteur)
        btn_del.clicked.connect(self.show_del_sauveteur)
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_del)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        return page

    def create_add_horaire_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(10)

        title = QLabel("ajouter horaire")
        layout.addWidget(title)

        form = QFormLayout()
        
        nom = QLineEdit()
        debut = QLineEdit()
        fin = QLineEdit()
        
        form.addRow("nom", nom)
        form.addRow("debut", debut)
        form.addRow("fin", fin)
        
        btn = QPushButton("ajouter")
        form.addRow("", btn)
        
        layout.addLayout(form)
        
        return page

    def create_del_horaire_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(10)

        title = QLabel("supprimer horaire")
        layout.addWidget(title)

        form = QFormLayout()
        
        nom = QLineEdit()
        debut = QLineEdit()
        fin = QLineEdit()
        
        form.addRow("Nom", nom)
        form.addRow("debut", debut)
        form.addRow("fin", fin)
        
        btn = QPushButton("supprimer")
        form.addRow("", btn)
        
        layout.addLayout(form)
        
        return page

    def create_add_sauveteur_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(10)

        title = QLabel("ajouter sauveteur")
        layout.addWidget(title)

        form = QFormLayout()
        
        nom = QLineEdit()
        prenom = QLineEdit()
        specialite = QLineEdit()
        departement = QLineEdit()
        
        form.addRow("Nom:", nom)
        form.addRow("Prenom:", prenom)
        form.addRow("Spécialité:", specialite)
        form.addRow("département:", departement)
        
        btn_layout = QHBoxLayout()
        btn_ajouter = QPushButton("ajouter")
        btn_retour = QPushButton("← Retour")
        btn_retour.clicked.connect(self.show_infos)
        
        btn_layout.addWidget(btn_ajouter)
        btn_layout.addWidget(btn_retour)
        btn_layout.addStretch()
        
        form.addRow("", btn_layout)
        layout.addLayout(form)
        
        return page

    def create_del_sauveteur_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(10)

        title = QLabel("supprimer sauveteur")
        layout.addWidget(title)

        form = QFormLayout()
        
        id_field = QLineEdit()
        form.addRow("Id", id_field)
        
        btn_layout = QHBoxLayout()
        btn_supprimer = QPushButton("supprimer")
        btn_retour = QPushButton("← Retour")
        btn_retour.clicked.connect(self.show_infos)
        
        btn_layout.addWidget(btn_supprimer)
        btn_layout.addWidget(btn_retour)
        btn_layout.addStretch()
        
        form.addRow("", btn_layout)
        layout.addLayout(form)
        
        return page

    # Actions
    def show_infos(self):
        self.stack.setCurrentWidget(self.page_infos)

    def show_add_horaire(self):
        self.stack.setCurrentWidget(self.page_add_horaire)

    def show_del_horaire(self):
        self.stack.setCurrentWidget(self.page_del_horaire)

    def show_add_sauveteur(self):
        self.stack.setCurrentWidget(self.page_add_sauveteur)

    def show_del_sauveteur(self):
        self.stack.setCurrentWidget(self.page_del_sauveteur)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())