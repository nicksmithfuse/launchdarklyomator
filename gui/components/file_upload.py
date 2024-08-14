from PyQt5.QtWidgets import QPushButton, QFileDialog
from utils.error_handler import error_handler

class FileUpload(QPushButton):
    def __init__(self):
        super().__init__("Upload File")
        self.clicked.connect(self.open_file_dialog)
        self.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
            }
        """)
        self.file_path = None

    def open_file_dialog(self):
        try:
            file_dialog = QFileDialog()
            self.file_path, _ = file_dialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
            if self.file_path:
                self.setText(f"File selected: {self.file_path.split('/')[-1]}")
                error_handler.log_info(f"File selected: {self.file_path}")
            else:
                error_handler.log_info("No file selected")
        except Exception as e:
            error_handler.handle_error(e, "Error in file selection")