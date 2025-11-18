"""
General methods to interact with the mongo database
"""

import bson
from bson import ObjectId
from pymongo.synchronous.client_session import ClientSession

from accelerator_core.schema.models.base_model import (
    TechnicalMetadataHistory,
    DisseminationLinkReport,
)
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.utils.accel_exceptions import AccelDocumentNotFoundException
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.logger import setup_logger
from bson.json_util import loads
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS

from accelerator_core.utils.mongo_tools import convert_doc_to_json

logger = setup_logger("accelerator")


class AccelDatabaseUtils:

    def __init__(
        self, accelerator_config: AcceleratorConfig, accel_db_context: AccelDbContext
    ):
        """
        Initialize the Accession sservice
        :param accelerator_config: AcceleratorConfig with general configuration
        :param accel_db_context: AccelDbContext that holds the db connection
        """
        self.accelerator_config = accelerator_config
        self.accel_db_context = accel_db_context

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
        :throws AccelDocumentNotFoundException: if the document is not found
        """

        logger.info(f"find_by_id({document_id}) is temp doc? {temp_doc}")

        db = self.connect_to_db()
        coll = self.build_collection_reference(document_type, temp_doc=False)
        doc = coll.find_one({"_id": ObjectId(document_id)})
        if not doc:
            raise AccelDocumentNotFoundException(document_id, document_type, temp_doc)

        doc = convert_doc_to_json(doc)
        return doc

    def connect_to_db(self):
        return self.accel_db_context.db

    def build_collection_reference(self, document_type: str, temp_doc: bool = False):
        """
        Find the correct collection based on the document type information in the ingest_source_descriptor
        :param document_type: type of the document, per the type matrix
        :param temp_doc: bool is True if this is a temporary document
        :return: the mongo collection
        """

        db = self.connect_to_db()

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

    def log_document_event(
        self,
        document_id: str,
        event: TechnicalMetadataHistory,
        document_type: str,
        temp_doc: bool = False,
    ):
        """
        Add the event to the database log
        :param document_id: unique id for the document (database doc id)
        :param event: the event to be logged
        :param document_type: type of the document, per the type matrix
        :param temp_doc: bool is True if this is a temporary document

        """

        update_operation = {"$push": {"technical_metadata.history": event.to_dict()}}

        logger.info("update_operation is %s", update_operation)
        collection = self.build_collection_reference(document_type, temp_doc)

        with self.accel_db_context.start_session() as session:
            with session.start_transaction():
                try:

                    doc = collection.find_one({"_id": ObjectId(document_id)})
                    if doc:
                        logger.info(f"Document {document_id} found before update.")
                    else:
                        logger.warning(
                            f"Document {document_id} NOT found before update."
                        )
                        raise Exception(
                            f"Document {document_id} NOT found before update."
                        )

                    result = collection.update_one(
                        {"_id": ObjectId(document_id)}, update_operation
                    )

                    if result.modified_count > 0:
                        logger.info(
                            f"Successfully updated document {document_id} with event."
                        )
                    else:
                        logger.warning(
                            f"No documents updated for {document_id}. Possible no match or no change."
                        )
                except Exception as e:
                    # Transaction is automatically aborted if an exception occurred within the 'with' block
                    print(f"Transaction aborted due to an error: {e}")
