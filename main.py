import sys
import logging
import traceback
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

logging.basicConfig(level=logging.ERROR)


try:
    def main():
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())


    if __name__ == "__main__":
        main()
except Exception as e:
    logging.error("An error occurred:")
    logging.error(traceback.format_exc())