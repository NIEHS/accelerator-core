"""
Dissemination support concrete implementation for Mongo data store
"""

import logging
from io import UnsupportedOperation

from accelerator_core.schema.models.base_model import (
    create_timestamped_log,
)
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.services.dissemination import (
    Dissemination,
    DisseminationDescriptor,
    DisseminationPayload,
)
from accelerator_core.utils.accel_database_utils import AccelDatabaseUtils
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.mongo_tools import convert_doc_to_json
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from utils.data_utils import generate_guid

logger = logging.getLogger(__name__)


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
        Disseminate an individual document, identified by its type (parent collection) and its id in the accelerator
        database
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

    def disseminate_by_original_source_and_id(
        self,
        original_source: str,
        original_document_identifier,
        dissemination_request: DisseminationDescriptor,
    ) -> DisseminationPayload:
        """
        This method is used for creating a dissemination payload by applying a filter
        that selects specific documents. The filtering mechanism is determined by the
        implementation and works on provided source and document identifiers. This is meant to return a single
        document based on its original source (e.g. "cedar") and the original identifier (e.g. the document DOI in cedar).

        This is distinguised from the dissemination_by_id method which is meant to return a single document based on its
        accelerator database identifier.

        Parameters:
            original_source: str
                The originating source of the document, used to identify the context or
                source system of the document.
            original_document_identifier
                The unique identifier of the document associated with the original source.
            dissemination_request: DisseminationDescriptor
                The object encapsulating metadata, rules, and instructions for how the document
                should be disseminated.

        Returns:
            DisseminationPayload
                The resulting payload from the dissemination operation, containing the processed
                document and relevant dissemination metadata.
        """

        logger.info(
            f"Disseminating document based on original source: {original_source} and document identifier: {original_document_identifier} of type {dissemination_request.ingest_type} to target: {dissemination_request.dissemination_type}"
        )

        doc = self.accel_database_utils.find_doc_by_original_source_identifier(
            dissemination_request.ingest_type,
            original_source,
            original_document_identifier,
            dissemination_request.temp_collection,
        )

        if doc is None:
            logger.warning(
                f"Document not found for original source: {original_source} and document identifier: {original_document_identifier} "
            )
            raise Exception(
                f"Document not found for original source: {original_source} and document identifier: {original_document_identifier} "
            )

        doc_id = AccelDatabaseUtils.extract_id_from_doc(doc)

        event = create_timestamped_log(
            f"Disseminating document  original source: {original_source} and document identifier: {original_document_identifier} as doc_id: {doc_id} of type {dissemination_request.ingest_type} to target: {dissemination_request.dissemination_type}"
        )

        dissemination_request.dissemination_item_id = doc_id

        self.accel_database_utils.log_document_event(
            doc_id,
            event,
            dissemination_request.ingest_type,
            dissemination_request.temp_collection,
        )

        doc = convert_doc_to_json(doc)

        dissemination_payload = DisseminationPayload(dissemination_request)
        self.report_individual_dissemination(dissemination_payload, doc_id, doc)
        dissemination_payload.dissemination_successful = True
        return dissemination_payload

    def disseminate_by_filter(
        self,
        dissemination_request: DisseminationDescriptor,
    ) -> [DisseminationPayload]:
        """
        Apply the given filter to create a set of documents to be disseminated to a target
        @param filter: DisseminationFilter that will select documents to disseminate. The internal meaning
        of the filter is dependent on the particular implementation

        Note that this method does not update the database indicating a dissemination, and it returns multiple documents.
        In normal usage patterns, the caller would use the result payloads to expand into individual dissemination tasks,
        and in those individual task calls, the caller would invoke the disseminate by id method to disseminate each document.

        @param dissemination_request: DisseminationRequest that describes the type, version, and other information
        @return: array of documents as DisseminationPayload
        """

        if not dissemination_request:
            raise Exception(
                "no dissemination_request provided to disseminate_by_filter, cannot continue"
            )

        if not dissemination_request.dissemination_filter:
            raise Exception(
                "no dissemination_filter provided to disseminate_by_filter, cannot continue"
            )

        docs = self.accel_database_utils.find_by_filter(
            dissemination_request.ingest_type,
            dissemination_request.dissemination_filter,
            dissemination_request.temp_collection,
        )
        if docs is None:
            logger.warning(
                f"No documents found for filter: {dissemination_request.dissemination_filter}"
            )

        payloads = []

        for doc in docs:
            guid = generate_guid()
            dissemination_request.dissemination_item_id = guid
            dissemination_payload = DisseminationPayload(dissemination_request)
            doc_id = AccelDatabaseUtils.extract_id_from_doc(doc)
            self.report_individual_dissemination(dissemination_payload, doc_id, doc)
            dissemination_payload.dissemination_successful = True
            payloads.append(dissemination_payload)

        return payloads

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
