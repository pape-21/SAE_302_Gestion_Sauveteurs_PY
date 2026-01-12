import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor 
from gestion_sauveteurs.database import DatabaseManager

class InterfacePlanning(QWidget):
    """Widget affichant le planning complet (lecture seule)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseManager()
        self.setWindowTitle("Planning Public")
        self.resize(900, 500) # Un peu plus large pour la nouvelle colonne

        self.setStyleSheet("background-color: #e9e4de;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        barre_titre = QLabel("Le Planning Opérationnel")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(40)
        barre_titre.setStyleSheet("background-color: #0b6fa4; color: white; font-weight: bold;")
        layout_principal.addWidget(barre_titre)

        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #ccc; gridline-color: #ccc; }
            QHeaderView::section { background-color: #0b6fa4; color: white; font-weight: bold; padding: 8px; }
        """)

        colonnes = ["Sauveteur", "Début", "Fin", "Mission", "Lieu"]
        self.table.setColumnCount(len(colonnes))
        self.table.setHorizontalHeaderLabels(colonnes)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        layout_principal.addWidget(self.table)
        
        self.charger_donnees()

    def charger_donnees(self):
        """Récupère tout le planning avec la localité."""
        conn = self.db_manager.get_connection()
        conn.row_factory = None
        cursor = conn.cursor()
        try:
            sql = """
                SELECT s.nom || ' ' || s.prenom, p.heure_debut, p.heure_fin, p.statut_mission, p.lieu
                FROM planning p
                JOIN sauveteur s ON p.sauveteur_id = s.id
                ORDER BY p.heure_debut ASC
            """
            cursor.execute(sql)
            lignes = cursor.fetchall()
            
            self.table.setRowCount(0)
            for i, data in enumerate(lignes):
                self.table.insertRow(i)
                
                statut_texte = str(data[3]).lower()
                couleur_fond = QColor("white")
                
                if "disponible" in statut_texte:
                    couleur_fond = QColor("lightgreen")
                elif "approche" in statut_texte:
                    couleur_fond = QColor("violet")
                elif "sous terre" in statut_texte:
                    couleur_fond = QColor("tan")
                elif "gestion" in statut_texte:
                    couleur_fond = QColor("yellow")
                elif "extérieur" in statut_texte or "exterieur" in statut_texte:
                    couleur_fond = QColor("orange")
                elif "repos" in statut_texte:
                    couleur_fond = QColor("lightblue")
                elif "brancardage" in statut_texte or "civière" in statut_texte:
                    couleur_fond = QColor("salmon")

                for j, val in enumerate(data):

                    texte_cellule = str(val) if val is not None else ""
                    
                    item = QTableWidgetItem(texte_cellule)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(couleur_fond)
                    self.table.setItem(i, j, item)
                    
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur BDD : {e}")
        finally:
            conn.close()

def lancer_planning_public():
    """Lance le planning en mode lecture seule."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        
    fenetre = InterfacePlanning()
    fenetre.show()
    app.exec_()

if __name__ == "__main__":
    lancer_planning_public()