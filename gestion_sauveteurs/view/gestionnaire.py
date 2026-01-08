import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QTableWidget, QLineEdit,
    QFormLayout, QStackedWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QComboBox, QDateTimeEdit, QDialog
)
from PyQt5.QtCore import Qt, QDateTime

# Imports Backend
from gestion_sauveteurs.crud.sauveteur import SauveteurCRUD
from gestion_sauveteurs.crud.planning import PlanningCRUD
from gestion_sauveteurs.view.planning_public import InterfacePlanning

# --- NOUVELLE CLASSE : Dialogue de suppression ---
class DialogueSupprimerMission(QDialog):
    """Dialogue modal pour supprimer une mission par son ID."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Supprimer une mission")
        self.setFixedSize(300, 150)
        self.crud_planning = PlanningCRUD()

        lbl_titre = QLabel("Suppression Mission", self)
        lbl_titre.setAlignment(Qt.AlignCenter)
        lbl_titre.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; padding: 5px;")
        lbl_titre.setGeometry(0, 0, 300, 30)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 40, 20, 20)
        
        layout_h = QHBoxLayout()
        layout_h.addWidget(QLabel("ID de la mission :"))
        self.champ_id = QLineEdit()
        self.champ_id.setPlaceholderText("Ex: 42")
        layout_h.addWidget(self.champ_id)
        layout.addLayout(layout_h)

        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_supprimer.setStyleSheet("background-color: #d32f2f; color: white;")
        self.btn_supprimer.clicked.connect(self.action_supprimer)
        layout.addWidget(self.btn_supprimer)

        self.setLayout(layout)

    def action_supprimer(self):
        id_mission = self.champ_id.text()
        if id_mission:
            if self.crud_planning.supprimer_mission(id_mission):
                QMessageBox.information(self, "Succès", f"Mission {id_mission} supprimée.")
                self.accept()
            else:
                QMessageBox.warning(self, "Erreur", "ID introuvable ou erreur BDD.")
        else:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un ID.")


class MainWindow(QMainWindow):
    """Fenêtre principale de l'espace Gestionnaire."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Espace Gestionnaire")
        self.resize(1000, 600)
        
        self.crud_sauveteur = SauveteurCRUD()
        self.crud_planning = PlanningCRUD()

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # ===== MENU GAUCHE =====
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.setSpacing(5)

        menu_label = QLabel("Gestionnaire")
        menu_label.setAlignment(Qt.AlignCenter)
        menu_label.setFixedHeight(40)
        menu_label.setStyleSheet("background-color: #0b6fa4; color: white; font-weight: bold;")
        menu_layout.addWidget(menu_label)

        self.btn_infos = QPushButton("informations générales")
        self.btn_add_h = QPushButton("ajouter horaire")
        
        self.btn_infos.clicked.connect(self.show_infos)
        self.btn_add_h.clicked.connect(self.show_add_horaire)

        for btn in [self.btn_infos, self.btn_add_h]:
            btn.setFixedHeight(40)
            menu_layout.addWidget(btn)

        menu_layout.addStretch()

        # ===== ZONE CENTRALE (Stack) =====
        self.stack = QStackedWidget()
        self.page_infos = self.create_infos_page()
        self.stack.addWidget(self.page_infos)
        self.page_add_horaire = self.create_add_horaire_page()
        self.stack.addWidget(self.page_add_horaire)
        self.page_add_sauveteur = self.create_add_sauveteur_page()
        self.stack.addWidget(self.page_add_sauveteur)

        self.stack.setCurrentWidget(self.page_infos)

        # ===== PLANNING (Bas) =====
        self.planning_widget = InterfacePlanning()

        # Bouton supprimer mission
        self.btn_del_mission = QPushButton("🗑️ Supprimer une mission (via ID)")
        self.btn_del_mission.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; padding: 8px;")
        self.btn_del_mission.clicked.connect(self.ouvrir_suppression_mission)

        # Assemblage final
        main_layout.addWidget(menu_widget, 1)
        
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.stack, 2)
        right_layout.addWidget(self.planning_widget, 2)
        right_layout.addWidget(self.btn_del_mission)
        
        main_layout.addLayout(right_layout, 4)

        self.setCentralWidget(main_widget)
        self.charger_tableau_sauveteurs()

    # ... (Les méthodes create_page et actions restent identiques) ...
    # Je ne les répète pas toutes ici pour la lisibilité, mais assure-toi
    # qu'elles sont bien présentes (create_infos_page, show_infos, etc.)

    def create_infos_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Informations Générales (Sauveteurs)")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        self.table_sauveteurs = QTableWidget()
        colonnes = ["ID", "Nom", "Prenom", "Spécialité", "Département"]
        self.table_sauveteurs.setColumnCount(len(colonnes))
        self.table_sauveteurs.setHorizontalHeaderLabels(colonnes)
        self.table_sauveteurs.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_sauveteurs)
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Ajouter Sauveteur")
        btn_del = QPushButton("Supprimer Sauveteur")
        btn_add.clicked.connect(self.show_add_sauveteur)
        btn_del.clicked.connect(self.action_supprimer_sauveteur)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_del)
        layout.addLayout(btn_layout)
        return page

    def create_add_horaire_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Ajouter une Mission / Horaire")
        layout.addWidget(title)
        form = QFormLayout()
        self.combo_sauv_mission = QComboBox()
        self.date_debut = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_fin = QDateTimeEdit(QDateTime.currentDateTime().addSecs(3600))
        self.input_mission = QLineEdit()
        self.input_mission.setPlaceholderText("Ex: Surveillance Plage")
        form.addRow("Sauveteur:", self.combo_sauv_mission)
        form.addRow("Début:", self.date_debut)
        form.addRow("Fin:", self.date_fin)
        form.addRow("Mission:", self.input_mission)
        btn_valider = QPushButton("Ajouter au planning")
        btn_valider.clicked.connect(self.action_valider_mission)
        form.addRow("", btn_valider)
        layout.addLayout(form)
        return page

    def create_add_sauveteur_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Nouveau Sauveteur")
        layout.addWidget(title)
        form = QFormLayout()
        self.input_nom = QLineEdit()
        self.input_prenom = QLineEdit()
        self.input_spec = QLineEdit()
        self.input_dep = QLineEdit()
        form.addRow("Nom:", self.input_nom)
        form.addRow("Prénom:", self.input_prenom)
        form.addRow("Spécialité:", self.input_spec)
        form.addRow("Département:", self.input_dep)
        btn_box = QHBoxLayout()
        btn_add = QPushButton("Enregistrer")
        btn_add.clicked.connect(self.action_valider_sauveteur)
        btn_back = QPushButton("Annuler")
        btn_back.clicked.connect(self.show_infos)
        btn_box.addWidget(btn_add)
        btn_box.addWidget(btn_back)
        layout.addLayout(form)
        layout.addLayout(btn_box)
        layout.addStretch()
        return page

    def show_infos(self):
        self.charger_tableau_sauveteurs()
        self.stack.setCurrentWidget(self.page_infos)

    def show_add_horaire(self):
        self.combo_sauv_mission.clear()
        sauveteurs = self.crud_sauveteur.get_tous()
        for s in sauveteurs:
            self.combo_sauv_mission.addItem(f"{s['nom']} {s['prenom']}", s['id'])
        self.stack.setCurrentWidget(self.page_add_horaire)

    def show_add_sauveteur(self):
        self.stack.setCurrentWidget(self.page_add_sauveteur)

    def action_valider_sauveteur(self):
        nom = self.input_nom.text()
        prenom = self.input_prenom.text()
        spec = self.input_spec.text()
        dep = self.input_dep.text()
        if nom and prenom:
            self.crud_sauveteur.ajouter(nom, prenom, dep, spec)
            QMessageBox.information(self, "OK", "Sauveteur ajouté")
            self.input_nom.clear(); self.input_prenom.clear()
            self.show_infos()
        else:
            QMessageBox.warning(self, "Erreur", "Champs obligatoires manquants")

    def action_valider_mission(self):
        sauv_id = self.combo_sauv_mission.currentData()
        debut = self.date_debut.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        fin = self.date_fin.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        mission = self.input_mission.text()
        if sauv_id:
            self.crud_planning.ajouter_mission(sauv_id, debut, fin, mission)
            QMessageBox.information(self, "OK", "Mission ajoutée")
            self.planning_widget.charger_donnees() 
        else:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un sauveteur")

    def action_supprimer_sauveteur(self):
        row = self.table_sauveteurs.currentRow()
        if row >= 0:
            id_sauv = self.table_sauveteurs.item(row, 0).text()
            nom = self.table_sauveteurs.item(row, 1).text()
            if QMessageBox.question(self, "Confirm", f"Supprimer {nom} ?") == QMessageBox.Yes:
                self.crud_sauveteur.supprimer(id_sauv)
                self.charger_tableau_sauveteurs()
        else:
            QMessageBox.warning(self, "Attention", "Sélectionnez une ligne")

    def charger_tableau_sauveteurs(self):
        data = self.crud_sauveteur.get_tous()
        self.table_sauveteurs.setRowCount(0)
        for i, s in enumerate(data):
            self.table_sauveteurs.insertRow(i)
            self.table_sauveteurs.setItem(i, 0, QTableWidgetItem(str(s['id'])))
            self.table_sauveteurs.setItem(i, 1, QTableWidgetItem(s['nom']))
            self.table_sauveteurs.setItem(i, 2, QTableWidgetItem(s['prenom']))
            self.table_sauveteurs.setItem(i, 3, QTableWidgetItem(s['specialite']))
            self.table_sauveteurs.setItem(i, 4, QTableWidgetItem(s['departement']))

    def ouvrir_suppression_mission(self):
        dialog = DialogueSupprimerMission(self)
        if dialog.exec_():
            self.planning_widget.charger_donnees()

# --- FONCTION DE LANCEMENT (Ajoutée) ---
def lancer_gestionnaire():
    """Lance l'interface Gestionnaire de manière bloquante."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    fenetre = MainWindow()
    fenetre.show()
    app.exec_()

if __name__ == "__main__":
    lancer_gestionnaire()