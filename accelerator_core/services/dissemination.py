from accelerator_core.utils.accelerator_config import AcceleratorConfig


class Dissemination:
    """Retrieves data from the database and transforms it into a JSON document for endpoint systems."""

    def __init__(self, accelerator_config: AcceleratorConfig):
        """Initialize Accession with validated data."""
        self.accelerator_config = accelerator_config

    def disseminate(self) -> dict:
        """Retrieve data from the database."""
        pass

    def format_for_endpoint(self, system: str) -> dict:
        """Convert data into a format required by a specific endpoint (CHORDS, Navigator, CEDAR)."""
        pass

    def export(self, system: str) -> bool:
        """Send the formatted data to the respective system."""
        pass
