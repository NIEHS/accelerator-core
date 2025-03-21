from accelerator_core.workflow.accel_source_ingest import IngestSourceDescriptor
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.schema_tools import SchemaTools

logger = setup_logger("accelerator")


class Accession:
    """Handles validation and CRUD operations for metadata records."""

    def __init__(self, accelerator_config: AcceleratorConfig):
        """Initialize Accession with validated data."""
        self.accelerator_config = accelerator_config

    def validate(
        self, json_dict: dict, ingest_source_descriptor: IngestSourceDescriptor
    ) -> bool:
        """
        Validate the given json structure against the Accelerator schema
        :param json_dict: dict with json contents to validate
        :param ingest_source_descriptor: ingest source descriptor describing the type, schema,
        and other configuration
        :return: bool is True if valid
        """
        """Validate JSON output from Crosswalk."""
        logger.info(f"validate, based on schema {ingest_source_descriptor}")

        schema_tools = SchemaTools(self.accelerator_config)

        valid = schema_tools.validate_json_against_schema(
            json_dict,
            ingest_source_descriptor.ingest_type,
            ingest_source_descriptor.schema_version,
        )
        return valid

    def ingest(
        self,
        accel_document: dict,
        ingest_source_descriptor: IngestSourceDescriptor,
        check_duplicates: bool = True,
        temp_doc: bool = False,
    ) -> str:
        """
        Ingest the given document
        :param accel_document: dict which is the document structure
        :param ingest_source_descriptor: ingest source descriptor describing the type, schema,
        and other configuration
        :param check_duplicates: bool indicates whether pre-checks for duplicate data run
        :param temp_doc: bool indicates whether the document is temporary or not
        :return: str with id of the ingested document
        """
        pass

    def decommission(self, document_id: str, document_type: str):
        """
        Remove the doc from the AIP store, this is not for temporary docs
        :param document_id: unique id for the document
        :param document_type: the type of document to be decommissioned, per the type matrix
        """
        pass

    def delete_temp_document(self, document_id: str, document_type: str):
        """
        Remove a document from the temp collection
        :param document_id: unique id for the document
        :param document_type: the type of document to be decommissioned, per the type matrix
        """
        pass

    def find_by_id(
        self, document_id, document_type: str, temp_doc: bool = False
    ) -> dict:
        """
        Find the document by id, from either the AIP store or the temporary store
        :param document_id: unique id for the document
        :param temp_doc: bool indicates whether the document is temporary or not
        :return: dict with the document structure
        """
        pass
