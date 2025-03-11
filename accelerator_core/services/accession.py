import accelerator_core.utils.accelerator_config
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.schema_tools import (
    CURRENT_ACCEL_SCHEMA_VERSION,
    validate_json_against_schema,
)

logger = setup_logger("accelerator")


class Accession:
    """Handles validation and CRUD operations for metadata records."""

    def __init__(self, accelerator_config: AcceleratorConfig):
        """Initialize Accession with validated data."""
        self.accelerator_config = accelerator_config

    def validate(
        self, json_dict: dict, schema_version: str = CURRENT_ACCEL_SCHEMA_VERSION
    ) -> bool:
        """
        Validate the given json structure against the Accelerator schema
        :param json_dict: dict with json contents to validate
        :param schema_version: str with the appropriate schema version
        :return: bool is True if valid
        """
        """Validate JSON output from Crosswalk."""
        logger.info(f"validate, based on schema {schema_version}")
        valid = validate_json_against_schema(json_dict, schema_version)
        return valid

    def create(self) -> str:
        """Create a new record in the database."""
        pass

    def read(self, record_id: str) -> dict:
        """Retrieve a record from the database."""
        pass

    def update(self, record_id: str, new_data: dict) -> bool:
        """Update an existing record."""
        pass

    def delete(self, record_id: str) -> bool:
        """Delete a record from the database."""
        pass
