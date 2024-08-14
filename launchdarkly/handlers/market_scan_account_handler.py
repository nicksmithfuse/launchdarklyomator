from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
import requests

FLAG_KEY = "fi.storeConfig.marketScan.accountNumber"

def setup_ui(self, layout, ld_client, flag_key, variation_name, variation_value):
    dealer_id = self.dealer_id_input.text()
    if not dealer_id:
        layout.addWidget(QLabel("Please enter a Dealer ID in the main window."))
        return

    flag_info_layout = QHBoxLayout()
    flag_info_layout.addWidget(QLabel(f"Flag Key: {FLAG_KEY}"))
    layout.addLayout(flag_info_layout)

    layout.addWidget(QLabel(f"Dealer ID: {dealer_id}"))

    self.check_button = QPushButton("Check for Dealer ID")
    self.check_button.clicked.connect(lambda: check_dealer_id(self))
    layout.addWidget(self.check_button)

    marketscan_layout = QHBoxLayout()
    marketscan_layout.addWidget(QLabel("MarketScan ID:"))
    self.marketscan_input = QLineEdit()
    marketscan_layout.addWidget(self.marketscan_input)
    layout.addLayout(marketscan_layout)

    variation_name_layout = QHBoxLayout()
    variation_name_layout.addWidget(QLabel("Variation Name:"))
    self.variation_name_input = QLineEdit()
    variation_name_layout.addWidget(self.variation_name_input)
    layout.addLayout(variation_name_layout)

    self.create_variation_button = QPushButton("Create Variation")
    self.create_variation_button.clicked.connect(lambda: add_variation(ld_client, flag_key, variation_name,
                                                                       variation_value))
    layout.addWidget(self.create_variation_button)

    self.create_targeting_button = QPushButton("Create Targeting")
    self.create_targeting_button.clicked.connect(lambda: create_targeting_rule(ld_client, flag_key, dealer_id,
                                                                               variation_value))
    self.create_targeting_button.setEnabled(False)
    layout.addWidget(self.create_targeting_button)

def check_dealer_id(self):
    dealer_id = self.dealer_id_input.text()
    if not dealer_id:
        QMessageBox.warning(self, "Input Error", "Please enter a Dealer ID in the main window.")
        return

    variation = get_flag_value(self.ld_client, FLAG_KEY, dealer_id)

    if variation is not None:
        self.log_message(f"Found variation for Dealer {dealer_id}: {variation}")
        self.create_variation_button.setEnabled(False)
        self.create_targeting_button.setEnabled(True)
    else:
        self.log_message(f"No variation found for Dealer {dealer_id}")
        self.create_variation_button.setEnabled(True)
        self.create_targeting_button.setEnabled(False)


def get_flag_value(ld_client, flag_key, dealer_id):
    url = f"{ld_client.base_url}/flags/{ld_client.project_key}/{ld_client.environment}/features/{flag_key}"
    response = requests.get(url, headers=ld_client.headers)
    if response.status_code == 200:
        flag_data = response.json()
        for rule in flag_data.get('rules', []):
            if any(clause.get('attribute') == 'key' and dealer_id in clause.get('values', []) for clause in
                   rule.get('clauses', [])):
                variation_id = rule.get('variationId')
                for variation in flag_data.get('variations', []):
                    if variation.get('id') == variation_id:
                        return variation.get('value')
    return None

def add_variation(ld_client, flag_key, variation_name, variation_value):
    if ld_client is None:
        print("Error: ld_client is None. Unable to add variation.")
        return False

    url = f"{ld_client.base_url}/flags/{ld_client.project_key}/{ld_client.environment}/features/{flag_key}/variations"

    try:
        response = requests.get(url, headers=ld_client.headers)
        response.raise_for_status()
        flag_data = response.json()

        new_variation = {
            "name": variation_name,
            "value": variation_value
        }
        flag_data['variations'].append(new_variation)

        update_response = requests.patch(url, headers=ld_client.headers, json=flag_data)
        update_response.raise_for_status()

        return True
    except requests.RequestException as e:
        print(f"Error adding variation: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error adding variation: {str(e)}")
        return False


def get_variation_value(ld_client, flag_key, variation_name):
    url = f"{ld_client.base_url}/flags/{ld_client.project_key}/{ld_client.environment}/features/{flag_key}/variations"
    response = requests.get(url, headers=ld_client.headers)
    if response.status_code == 200:
        flag_data = response.json()
        for variation in flag_data.get('variations', []):
            if variation.get('name') == variation_name:
                return variation.get('value')
    return None


def create_targeting_rule(ld_client, flag_key, dealer_id, variation_value):
    url = f"{ld_client.base_url}/flags/{ld_client.project_key}/{ld_client.environment}/features/{flag_key}"

    try:
        response = requests.get(url, headers=ld_client.headers)
        response.raise_for_status()
        flag_data = response.json()

        variation_index = next((index for index, variation in enumerate(flag_data['variations'])
                                if variation['value'] == variation_value), None)

        if variation_index is None:
            print(f"No variation found with value: {variation_value}")
            return False

        new_rule = {
            "clauses": [
                {
                    "attribute": "key",
                    "op": "in",
                    "values": [dealer_id]
                }
            ],
            "variation": variation_index
        }

        flag_data['rules'].insert(0, new_rule)

        update_response = requests.patch(url, headers=ld_client.headers, json=flag_data)
        update_response.raise_for_status()

        return True
    except requests.RequestException as e:
        print(f"Error creating targeting rule: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error creating targeting rule: {str(e)}")
        return False