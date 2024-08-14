from PyQt5.QtWidgets import QCheckBox

class Checkbox(QCheckBox):
    def __init__(self, label):
        super().__init__(label)
        self.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)