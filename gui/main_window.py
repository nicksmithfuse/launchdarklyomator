from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QTextEdit, QPushButton,
                             QFrame, QSizePolicy, QListWidget, QStackedWidget, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from gui.components.checkbox import Checkbox
from gui.components.dropdown import Dropdown
from launchdarkly.api_client import LaunchDarklyAPIClient
from config.flag_definitions import desking_flags, desking_plus_flags, e2e_flags
from launchdarkly.flag_handlers import get_handler


import sys
import traceback
import logging

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LaunchDarkly Configuration Tool")
        self.setGeometry(100, 100, 1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # LaunchDarkly Connection Section
        ld_connection_layout = QHBoxLayout()
        self.connect_button = QPushButton("Connect to LaunchDarkly")
        self.connect_button.clicked.connect(self.connect_to_launchdarkly)
        self.environment_dropdown = Dropdown(["Test", "Production"])
        self.connection_status = QLabel("Not Connected")
        ld_connection_layout.addWidget(self.connect_button)
        ld_connection_layout.addWidget(self.environment_dropdown)
        ld_connection_layout.addWidget(self.connection_status)
        main_layout.addLayout(ld_connection_layout)

        # Top section
        top_section = QHBoxLayout()

        # Dealer ID input
        dealer_id_layout = QVBoxLayout()
        dealer_id_label = QLabel("Dealer ID:")
        self.dealer_id_input = QLineEdit()
        self.dealer_id_input.setFixedWidth(150)
        dealer_id_layout.addWidget(dealer_id_label)
        dealer_id_layout.addWidget(self.dealer_id_input)
        top_section.addLayout(dealer_id_layout)

        # Product tier dropdown
        product_tier_layout = QVBoxLayout()
        product_tier_label = QLabel("Product Tier:")
        self.product_tier_dropdown = Dropdown(["Select", "Desking", "Desking+", "E2E"])
        self.product_tier_dropdown.currentTextChanged.connect(self.on_product_tier_changed)
        product_tier_layout.addWidget(product_tier_label)
        product_tier_layout.addWidget(self.product_tier_dropdown)
        top_section.addLayout(product_tier_layout)

        # DR checkbox
        dr_layout = QVBoxLayout()
        dr_label = QLabel("DR:")
        self.dr_checkbox = Checkbox("")
        dr_layout.addWidget(dr_label)
        dr_layout.addWidget(self.dr_checkbox)
        top_section.addLayout(dr_layout)

        main_layout.addLayout(top_section)

        # Middle section
        middle_section = QHBoxLayout()

        # Flag list
        self.flag_list = QListWidget()
        self.flag_list.itemClicked.connect(self.on_flag_selected)
        middle_section.addWidget(self.flag_list, 1)

        # Flag configuration section
        self.flag_config_section = QStackedWidget()
        middle_section.addWidget(self.flag_config_section, 2)

        main_layout.addLayout(middle_section)

        # Log window
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        self.log_window.setFont(QFont("Courier", 10))
        self.log_window.setFixedHeight(100)
        main_layout.addWidget(self.log_window)

        self.ld_client = None
        self.current_flags = []
        self.current_flag_index = -1

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        error_message = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.critical("Unhandled exception: %s", error_message)
        self.log_message(f"Critical Error: {error_message}")
        QMessageBox.critical(self, "Critical Error", f"An unhandled exception occurred:\n{error_message}")
    def connect_to_launchdarkly(self):
        try:
            environment = self.environment_dropdown.currentText().lower()
            self.log_message(f"Connecting to LaunchDarkly {environment} environment...")
            self.ld_client = LaunchDarklyAPIClient(environment)
            if self.ld_client.test_connection():
                self.connection_status.setText(f"Connected to {environment}")
                self.log_message("Successfully connected to LaunchDarkly")
            else:
                self.connection_status.setText("Connection Failed")
                self.log_message("Failed to connect to LaunchDarkly. Check console for more details.")
        except Exception as e:
            self.log_message(f"Error in connect_to_launchdarkly: {str(e)}")
            self.log_message(f"Exception type: {type(e).__name__}")
            self.log_message(f"Exception traceback: {sys.exc_info()}")

    def on_product_tier_changed(self, product_tier):
        self.flag_list.clear()
        self.current_flags = []
        if product_tier == "Desking":
            self.current_flags = desking_flags.DESKING_FLAGS
        elif product_tier == "Desking+":
            self.current_flags = desking_plus_flags.DESKING_PLUS_FLAGS
        elif product_tier == "E2E":
            self.current_flags = e2e_flags.E2E_FLAGS

        for flag in self.current_flags:
            self.flag_list.addItem(flag.name)

    def on_flag_selected(self, item):
        try:
            flag_name = item.text()
            self.log_message(f"Flag selected: {flag_name}")
            flag = next((f for f in self.current_flags if f.name == flag_name), None)
            if flag:
                self.log_message(f"Displaying configuration for flag: {flag.key}")
                self.display_flag_config(flag)
            else:
                self.log_message(f"No flag found with name: {flag_name}")
        except Exception as e:
            error_message = f"Error in on_flag_selected: {str(e)}"
            logger.error(error_message)
            logger.error(traceback.format_exc())
            self.log_message(error_message)

    def display_flag_config(self, flag):
        try:
            while self.flag_config_section.count():
                self.flag_config_section.removeWidget(self.flag_config_section.widget(0))

            flag_widget = QWidget()
            layout = QVBoxLayout(flag_widget)

            layout.addWidget(QLabel(f"Flag Name: {flag.name}"))
            layout.addWidget(QLabel(f"Flag Key: {flag.key}"))

            handler = get_handler(flag.key)
            if handler:
                self.log_message(f"Calling handler for flag: {flag.key}")
                handler(self, layout, self.ld_client, flag.key, flag.name, None)
            else:
                self.log_message(f"No handler implemented for flag: {flag.key}")
                layout.addWidget(QLabel("Configuration for this flag is not yet implemented."))

            self.flag_config_section.addWidget(flag_widget)
            self.flag_config_section.setCurrentWidget(flag_widget)
        except Exception as e:
            error_message = f"Error in display_flag_config: {str(e)}"
            logger.error(error_message)
            logger.error(traceback.format_exc())
            self.log_message(error_message)

    def log_message(self, message):
        self.log_window.append(message)
        self.log_window.verticalScrollBar().setValue(
            self.log_window.verticalScrollBar().maximum()
        )