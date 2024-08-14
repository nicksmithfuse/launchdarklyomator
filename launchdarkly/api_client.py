import requests
import logging
from config.config import LD_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LaunchDarklyAPIClient:
    def __init__(self, environment, project_key="default"):
        self.api_key = LD_API_KEY
        self.project_key = project_key
        self.environment = environment.lower()
        self.base_url = "https://app.launchdarkly.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def test_connection(self):
        try:
            response = requests.get(f"{self.base_url}/projects/{self.project_key}", headers=self.headers)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_flag_configuration(self, flag_key):
        url = f"{self.base_url}/flags/{self.project_key}/{self.environment}/{flag_key}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to retrieve flag configuration. Status code: {response.status_code}")
        return None