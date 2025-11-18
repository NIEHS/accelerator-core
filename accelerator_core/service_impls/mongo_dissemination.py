"""
Dissemination support concrete implementation for Mongo data store
"""

from io import UnsupportedOperation

from bson import ObjectId
from pipenv.patched.safety.formatter import NOT_IMPLEMENTED

from accelerator_core.schema.models.base_model import (
    create_timestamped_log,
    DisseminationEndpoint,
)
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.services.dissemination import (
    Dissemination,
    DisseminationDescriptor,
    DisseminationPayload,
    DisseminationFilter,
)
from accelerator_core.utils.accel_database_utils import AccelDatabaseUtils
from accelerator_core.utils.accel_exceptions import AccelDocumentNotFoundException
from accelerator_core.utils.schema_tools import SchemaValidationResult
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_source_ingest import (
    IngestSourceDescriptor,
    IngestPayload,
)
from accelerator_core.services.accession import Accession
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.logger import setup_logger

logger = setup_logger("accelerator")


class DisseminationMongo(Dissemination):
    """
    Concrete implementation of Dissemination
    """

    def __init__(
        self,
        accelerator_config: AcceleratorConfig,
        xcom_properties_resolver: XcomPropsResolver,
        accel_db_context: AccelDbContext,
    ):
        """
        Initialize the Accession sservice
        @param accelerator_config: AcceleratorConfig with general configuration
        @param accel_db_context: AccelDbContext that holds the db connection
        """
        super().__init__(accelerator_config, xcom_properties_resolver)
        self.accel_db_context = accel_db_context
        self.accel_database_utils = AccelDatabaseUtils(
            accelerator_config, accel_db_context
        )

    def disseminate_by_id(
        self, document_id: str, dissemination_request: DisseminationDescriptor
    ) -> DisseminationPayload:
        """
        Disseminate an individual document, identified by its type (parent collection) and its id
        @param document_id: str with unique document id
        @param dissemination_request: DisseminationDescriptor that describes the type, version, and
        other information
        @return: DisseminationPayload with the resulting information
        """

        logger.info(f"Disseminating document {document_id}")

        doc = self.accel_database_utils.find_by_id(
            document_id,
            dissemination_request.ingest_type,
            temp_doc=dissemination_request.temp_collection,
        )

        if doc is None:
            logger.warning(f"Document {document_id} not found")
            raise Exception(f"Document {document_id} not found")

        event = create_timestamped_log(
            f"Disseminating document {document_id} of type {dissemination_request.ingest_type} to target: {dissemination_request.dissemination_type}"
        )

        self.accel_database_utils.log_document_event(
            str(document_id),
            event,
            dissemination_request.ingest_type,
            dissemination_request.temp_collection,
        )

        dissemination_payload = DisseminationPayload(dissemination_request)
        self.report_individual_dissemination(dissemination_payload, document_id, doc)
        dissemination_payload.dissemination_successful = True
        return dissemination_payload

    def disseminate_by_filter(
        self,
        filter: DisseminationFilter,
        dissemination_request: DisseminationDescriptor,
    ) -> [DisseminationPayload]:
        """
        Apply the given filter to create a set of documents to be disseminated to a target
        @param filter: DisseminationFilter that will select documents to disseminate. The internal meaning
        of the filter is dependent on the particular implementation
        @param dissemination_request: DisseminationRequest that describes the type, version, and other information
        @return: array of documents as DisseminationPayload
        """
        raise UnsupportedOperation("dissemination by filter not yet supported")

    def report_individual_dissemination(
        self, dissemination_payload: DisseminationPayload, item_id: str, item: dict
    ):
        """
        report an individual sub-result.

        This method will:
        * understand how to report the result
        * understand the location to which to write any temp data to pass along
        * keep track of the overall results in DisseminationPayload for close-out

        @param: dissemination_payload DisseminationPayload that will receive the new item, NB that the run_id should
            be provided in the DisseminationDescriptor that is part of the payload
        @param: item_id string that identifies the item to report
        @param: item dict that contains information about the item to report
        @return: None (DisseminationPayload will have the item appended in the correct fashion)

        """

        if not dissemination_payload.dissemination_descriptor.dissemination_identifier:
            raise Exception(
                "no dissemination_identifier (run_id) provided in descriptor"
            )

        if not item_id:
            raise Exception("no item_id provided")

        dissemination_payload.dissemination_descriptor.dissemination_item_id = item_id

        if not dissemination_payload.dissemination_descriptor.use_tempfiles:
            logger.debug("appending the item inline")
            dissemination_payload.payload.append(item)
            dissemination_payload.payload_inline = True
            return

        logger.info("processing individual result via temp file")
        stored_path = self.xcomUtils.store_dict_in_temp_file(
            item_id,
            item,
            dissemination_payload.dissemination_descriptor.dissemination_identifier,
        )

        logger.info(f"stored path: {stored_path}")
        dissemination_payload.payload_path.append(stored_path)
        dissemination_payload.payload_inline = False
