import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

class InterfacePlanning(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: #e9e4de;")
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        barre_titre = QLabel("Le Planning")
        barre_titre.setAlignment(Qt.AlignCenter)
        barre_titre.setFixedHeight(45)
        barre_titre.setStyleSheet("background-color: #1a6f91; color: white; font-weight: bold;")
        layout_principal.addWidget(barre_titre)

        layout_tableau = QVBoxLayout()
        layout_tableau.setContentsMargins(40, 40, 40, 40)

        self.table = QTableWidget(3, 7)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #4b89c5; gridline-color: #0d3b66; color: black; border: 2px solid #0d3b66; }
            QHeaderView::section { background-color: #4b89c5; border: 1px solid #0d3b66; font-weight: bold; }
        """)

        self.table.setHorizontalHeaderLabels(["10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30"])
        self.table.setVerticalHeaderLabels(["René lapin", "Albert Zorg", "Romain AL"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        item = QTableWidgetItem("pre")
        item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(1, 2, item)

        layout_tableau.addWidget(self.table)
        layout_principal.addLayout(layout_tableau)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = InterfacePlanning()
    fenetre.resize(1000, 500)
    fenetre.show()
    sys.exit(app.exec_())