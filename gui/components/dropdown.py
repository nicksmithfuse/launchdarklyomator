from PyQt5.QtWidgets import QComboBox

class Dropdown(QComboBox):
    def __init__(self, items):
        super().__init__()
        self.addItems(items)
        self.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                min-width: 150px;
                padding: 5px;
            }
        """)