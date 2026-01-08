import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from gestion_sauveteurs.database import DatabaseManager
from PyQt5.QtCore import QDateTime

class InterfacePlanning(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseManager()

        # --- STYLE ---
        self.setStyleSheet("background-color: #e9e4de;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # Bandeau Titre
        barre_titre = QLabel("Le Planning")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(40)
        barre_titre.setStyleSheet("background-color: #0b6fa4; color: white; font-weight: bold;")
        layout_principal.addWidget(barre_titre)

        # Tableau
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #ccc; gridline-color: #ccc; }
            QHeaderView::section { background-color: #0b6fa4; color: white; font-weight: bold; padding: 8px; }
        """)

        # Colonnes
        colonnes = ["Sauveteur", "Début", "Fin", "Mission"]
        self.table.setColumnCount(len(colonnes))
        self.table.setHorizontalHeaderLabels(colonnes)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        layout_principal.addWidget(self.table)
        
        # Chargement initial
        self.charger_donnees()

    def charger_donnees(self):
        """Récupère tout le planning."""
        conn = self.db_manager.get_connection()
        conn.row_factory = None # On veut des tuples pour l'indexation simple, ou gère le Row
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
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(i, j, item)
                    
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur BDD : {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fen = InterfacePlanning()
    fen.resize(800, 400)
    fen.show()
    sys.exit(app.exec_())