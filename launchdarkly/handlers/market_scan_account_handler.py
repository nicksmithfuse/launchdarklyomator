from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QTextEdit
import requests
import json

FLAG_KEY = "fi.storeConfig.marketScan.accountNumber"


def setup_ui(self, layout, ld_client, flag_key, flag_name, variation_value):

    fetch_button = QPushButton("Fetch Flag Configuration")
    fetch_button.clicked.connect(lambda: fetch_flag_config(self, ld_client))
    layout.addWidget(fetch_button)

    self.config_display = QTextEdit()
    self.config_display.setReadOnly(True)
    layout.addWidget(self.config_display)


def fetch_flag_config(self, ld_client):
    try:
        url = f"https://app.launchdarkly.com/api/v2/flags/{ld_client.project_key}/{FLAG_KEY}"
        headers = {
            "Authorization": ld_client.api_key,
            "Content-Type": "application/json"
        }

        self.log_message(f"Fetching flag configuration from: {url}")
        response = requests.get(url, headers=headers)

        self.log_message(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            flag_config = response.json()
            self.config_display.setPlainText(json.dumps(flag_config, indent=2))
            self.log_message(f"Successfully retrieved flag configuration for {FLAG_KEY}")
        else:
            error_message = f"Failed to retrieve flag configuration. Status code: {response.status_code}"
            self.config_display.setPlainText(error_message)
            self.log_message(error_message)
            self.log_message(f"Response content: {response.text}")

    except Exception as e:
        error_message = f"Error fetching flag configuration: {str(e)}"
        self.config_display.setPlainText(error_message)
        self.log_message(error_message)