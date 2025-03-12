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

    def ingest(
        self, acel_document: dict, check_duplicates: bool = True, temp_doc: bool = False
    ) -> str:
        """
        Ingest the given document
        :param acel_document: dict which is the document structure
        :param check_duplicates: bool indicates whether pre-checks for duplicate data run
        :param temp_doc: bool indicates whether the document is temporary or not
        :return: str with id of the ingested document
        """
        pass

    def decommission(self, document_id):
        """
        Remove the doc from the AIP store, this is not for temporary docs
        :param document_id: unique id for the document
        """
        pass

    def delete_temp_document(self, document_id):
        """
        Remove a document from the temp collection
        :param document_id:
        """
        pass

    def find_by_id(self, document_id, temp_doc: bool = False) -> dict:
        """
        Find the document by id, from either the AIP store or the temporary store
        :param document_id: unique id for the document
        :param temp_doc: bool indicates whether the document is temporary or not
        :return: dict with the document structure
        """
