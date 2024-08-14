from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

@dataclass
class Variation:
    # Represents a single variation of a flag
    name: str                       # Name of the variation
    value: Any                      # Value of the variation (can be any type)
    description: Optional[str] = None  # Optional description of the variation

@dataclass
class Flag:
    # Represents a LaunchDarkly feature flag
    key: str                        # Unique identifier for the flag
    name: str                       # Human-readable name of the flag
    description: str                # Description of the flag's purpose
    variations: List[Variation] = field(default_factory=list)  # List of possible variations for this flag
    default_variation: str = "default"  # Name of the default variation to use
    custom_handler: Optional[Callable] = None  # Custom function to handle this flag, if needed

    def get_variation(self, name):
        # Retrieve a specific variation by name
        return next((v for v in self.variations if v.name == name), None)

    def add_variation(self, name, value, description=None):
        # Add a new variation to this flag
        self.variations.append(Variation(name, value, description))

    def handle(self, dealer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Process the flag for a specific dealer
        if self.custom_handler:
            # Use the custom handler if one is defined
            return self.custom_handler(self, dealer_id, data)
        # Default handling logic if no custom handler is defined
        return {
            "key": self.key,
            "value": self.get_variation(self.default_variation).value
        }