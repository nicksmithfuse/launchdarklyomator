from typing import List, Dict, Any
from launchdarkly.flag import Flag
from config.flag_definitions import base_flags, desking_flags, desking_plus_flags, e2e_flags
from utils.error_handler import error_handler


# FlagManager orchestrates the process of applying flags:
# - It determines which flags to apply based on the configuration
# - Calls the appropriate handler for each flag (either custom or default)
# - Uses the API client to update the flags in LaunchDarkly

class FlagManager:
    def __init__(self, api_client):
        self.api_client = api_client
        self.configurations = {
            "Desking": desking_flags.DESKING_FLAGS,
            "Desking+": desking_plus_flags.DESKING_PLUS_FLAGS,
            "E2E": e2e_flags.E2E_FLAGS,
        }

    def get_flags_for_configuration(self, config_name: str) -> List[Flag]:
        # Retrieve the list of flags for a given configuration
        # Returns an empty list if the configuration doesn't exist
        return self.configurations.get(config_name, [])

    def apply_configuration(self, config_name: str, dealer_id: str, dr_enabled: bool, data: Dict[str, Any]):
        # Apply a configuration for a specific dealer
        # Retrieve flags for the given configuration
        flags = self.get_flags_for_configuration(config_name)

        # If DR is enabled, add DR flags to the list
        if dr_enabled:
            flags.extend(self.configurations["DR"])

        # Process each flag in the configuration
        for flag in flags:
            try:
                # Call the flag's handle method (custom or default)
                flag_data = flag.handle(dealer_id, data)
                # Update the flag value in LaunchDarkly using the API client
                self.api_client.update_flag_value(flag_data['key'], dealer_id, flag_data['value'])
                # Log successful update
                error_handler.log_info(f"Updated flag {flag.key} for dealer {dealer_id}")
            except Exception as e:
                # Log any errors that occur during flag update
                error_handler.handle_error(e, f"Error updating flag {flag.key} for dealer {dealer_id}")

