import logging
from PyQt5.QtCore import QObject, pyqtSignal

class ErrorHandler(QObject):
    error_occurred = pyqtSignal(str)
    info_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename='app.log')
        self.logger = logging.getLogger()

    def handle_error(self, error, message):
        full_message = f"ERROR: {message}: {str(error)}"
        self.logger.error(full_message)
        self.error_occurred.emit(full_message)

    def log_info(self, message):
        self.logger.info(message)
        self.info_occurred.emit(f"INFO: {message}")

error_handler = ErrorHandler()