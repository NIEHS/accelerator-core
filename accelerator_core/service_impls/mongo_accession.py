"""
Accession support concrete implementation for Mongo data store
"""

from bson import ObjectId

from accelerator_core.schema.models.base_model import (
    create_timestamped_log,
    get_time_now_iso,
)
from accelerator_core.service_impls.accel_db_context import AccelDbContext
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

"""
TODO: delegate calls to accel_database_utils - mc
"""


class AccessionMongo(Accession):
    """
    Accession module based on Mongo persistence
    """

    def __init__(
        self,
        accelerator_config: AcceleratorConfig,
        accel_db_context: AccelDbContext,
        xcom_properties_resolver: XcomPropsResolver,
    ):
        """
        Initialize the Accession sservice
        :param accelerator_config: AcceleratorConfig with general configuration
        :param accel_db_context: AccelDbContext that holds the db connection
        :param xcom_properties_resolver: XcomPropertiesResolver injects utilities for
        resolving payload
        """
        super().__init__(accelerator_config, xcom_properties_resolver)
        self.accel_db_context = accel_db_context

    def validate(
        self, json_dict: dict, ingest_source_descriptor: IngestSourceDescriptor
    ) -> SchemaValidationResult:
        return super().validate(json_dict, ingest_source_descriptor)

    def ingest(
        self,
        ingest_payload: IngestPayload,
        check_duplicates: bool = True,
        temp_doc: bool = False,
    ) -> str:
        """
        Ingest the given document
        :param ingest_payload: ingest source descriptor describing the type, schema,
        and other configuration along with a payload (either in-line or a path to a document)
        :param check_duplicates: bool indicates whether pre-checks for duplicate data run
        :param temp_doc: bool indicates whether the document is temporary or not
        :return: str with id of the ingested document
        """
        logger.info("ingest()")

        payload_length = self.get_payload_length(ingest_payload)

        if payload_length == 0:
            logger.info("no payload to ingest")
            return ""
        elif payload_length > 1:
            # TODO: refactor to support multiple ingest, will require api change to return payload
            raise Exception("currently only supports one doc per ingest")

        db = self.connect_to_db()
        coll = self.build_collection_reference(
            db, ingest_payload.ingest_source_descriptor.ingest_type, temp_doc
        )

        doc = self.payload_resolve(ingest_payload, 0)

        # TODO: add check for update versus insert - mcc

        # look for technical metadata and add log message
        technical_metadata = doc.get("technical_metadata", None)
        if technical_metadata:
            technical_metadata["created"] = get_time_now_iso()
            technical_metadata["original_source"] = (
                ingest_payload.ingest_source_descriptor.ingest_item_id
            )
            technical_metadata["original_source_link"] = (
                ingest_payload.ingest_source_descriptor.ingest_link
            )
            technical_metadata["history"].append(
                create_timestamped_log(
                    f"accession from {ingest_payload.ingest_source_descriptor.ingest_type} with identifier {ingest_payload.ingest_source_descriptor.ingest_item_id} in operation {ingest_payload.ingest_source_descriptor.ingest_identifier}"
                ).to_dict()
            )

        result = self.validate(doc, ingest_payload.ingest_source_descriptor)
        if not result.valid:
            raise Exception(f"Invalid document provided {result.error_message}")

        id = coll.insert_one(doc).inserted_id

        logger.info(f"inserted id {id}")
        return id

    def decommission(
        self,
        document_id: str,
        document_type: str,
    ):
        """
        Remove a document from the temp collection
        :param document_id: unique id for the document
        :param document_type: the type of document to be decommissioned, per the type matrix
        """
        logger.info(f"decommission({document_id} of type {document_type})")

        type_matrix_info = self.accelerator_config.find_type_matrix_info_for_type(
            document_type
        )
        if not type_matrix_info:
            raise Exception(f"unknown type {document_type}")

        db = self.connect_to_db()
        coll = self.build_collection_reference(db, document_type)
        delete_result = coll.delete_one(
            {"_id": ObjectId(document_id)}
        )  # TODO:think of a trash can model
        logger.info(f"deleted id {delete_result}")

    def delete_temp_document(self, document_id: str, document_type: str):
        """
        Remove a document from the temp collection
        :param document_id: unique id for the document
        :param document_type: the type of document to be decommissioned, per the type matrix
        """
        logger.info(f"delete_temp_document({document_id})")

        db = self.connect_to_db()
        coll = self.build_collection_reference(db, document_type, temp_doc=True)
        delete_result = coll.delete_one({"_id": ObjectId(document_id)})
        logger.info(f"deleted id {delete_result}")

    def find_by_id(
        self, document_id: str, document_type: str, temp_doc: bool = False
    ) -> dict:
        """
        Find the document by id, from either the AIP store or the temporary store
        :param document_id: unique id for the document
        :param document_type type of document per type matrix
        :param temp_doc: bool indicates whether the document is temporary or not
        :return: dict with the document structure
        """

        logger.info(f"find_by_id({document_id}) is temp doc? {temp_doc}")

        db = self.connect_to_db()
        coll = self.build_collection_reference(db, document_type, temp_doc=False)
        doc = coll.find_one({"_id": ObjectId(document_id)})
        return doc

    def connect_to_db(self):
        return self.accel_db_context.db

    def build_collection_reference(
        self, db, document_type: str, temp_doc: bool = False
    ):
        """
        Find the correct collection based on the document type information in the ingest_source_descriptor
        :param db: Mongo db
        :param document_type: type of the document, per the type matrix
        :param temp_doc: bool is True if this is a temporary document
        :return: the mongo collection
        """

        type_matrix_info = self.accelerator_config.find_type_matrix_info_for_type(
            document_type
        )
        if not type_matrix_info:
            raise Exception(f"unknown type {document_type}")

        if temp_doc:
            coll_name = type_matrix_info.temp_collection
        else:
            coll_name = type_matrix_info.collection

        return db[coll_name]
