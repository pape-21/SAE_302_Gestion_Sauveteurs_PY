import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox, QPushButton)
from PyQt5.QtCore import Qt
from gestion_sauveteurs.database import DatabaseManager

class InterfacePlanning(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.db_manager = DatabaseManager() # <--- Ajout Backend

        # --- STYLE DE SOKHNA ---
        self.setStyleSheet("background-color: #e9e4de;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # Bandeau Titre (Sokhna)
        barre_titre = QLabel("Le Planning")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(45)
        barre_titre.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold;")
        layout_principal.addWidget(barre_titre)

        layout_tableau = QVBoxLayout()
        layout_tableau.setContentsMargins(40, 40, 40, 40)

        # --- TABLEAU ---
        # On garde son style CSS exact, mais on adapte les colonnes aux données BDD
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget { background-color: #4b89c5; gridline-color: #0d3b66; color: black; border: 2px solid #0d3b66; }
            QHeaderView::section { background-color: #4b89c5; border: 1px solid #0d3b66; font-weight: bold; }
        """)

        # Colonnes adaptées à ta BDD
        colonnes = ["Sauveteur", "Début", "Fin", "Mission"]
        self.table.setColumnCount(len(colonnes))
        self.table.setHorizontalHeaderLabels(colonnes)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False) # On cache les numéros de ligne

        layout_tableau.addWidget(self.table)
        layout_principal.addLayout(layout_tableau)
        
        # Bouton Fermer (Ajout pratique pour fermer la fenêtre popup)
        self.btn_fermer = QPushButton("Fermer")
        self.btn_fermer.clicked.connect(self.close)
        # On lui donne un style proche du thème
        self.btn_fermer.setStyleSheet("background-color: #1a6f91; color: white; padding: 5px;") 
        layout_tableau.addWidget(self.btn_fermer)

        # --- CHARGEMENT DONNÉES ---
        self.charger_donnees()

    def charger_donnees(self):
        """Récupère les données via SQL et remplit le tableau (Logique Pape)."""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                SELECT s.nom || ' ' || s.prenom, p.heure_debut, p.heure_fin, p.statut_mission
                FROM planning p
                JOIN sauveteur s ON p.sauveteur_id = s.id
                ORDER BY p.heure_debut ASC
            """
            cursor.execute(sql)
            lignes = cursor.fetchall()
            
            self.table.setRowCount(0)
            for i, data in enumerate(lignes):
                self.table.insertRow(i)
                for j, val in enumerate(data):
                    item = QTableWidgetItem(str(val))
                    item.setTextAlignment(Qt.AlignCenter) # Centré comme Sokhna le voulait
                    self.table.setItem(i, j, item)
                    
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur BDD : {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = InterfacePlanning()
    fenetre.resize(1000, 500)
    fenetre.show()
    sys.exit(app.exec_())