from PyQt5.QtWidgets import QPushButton

class BoutonRefresh(QPushButton):
    def __init__(self, callback):
        super().__init__("🔄 Actualiser la liste")
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.clicked.connect(callback)
