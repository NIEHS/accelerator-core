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

    def clear_collection(self, document_type: str, temp_doc=False):
        """
        DANGER! This method is used to support unit testing, and clears all documents in the given
        collection. It should not be used in production.
        :param document_type: the type of document to be cleared, per the type matrix\
        :param temp_doc: bool indicates whether the document is temporary or not
        """

        db = self.connect_to_db()
        coll = self.build_collection_reference(document_type, temp_doc=temp_doc)
        coll.delete_many({})

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

    def find_doc_by_original_source_identifier(
        self,
        ingest_type: str,
        original_source_link: str,
        original_source_identifier: str,
        temp_doc: bool = False,
    ) -> dict:
        """
        Find a document based on the given original source link and identifier.

        This method searches for a document in the database using the provided
        original source link and original source identifier. The optional
        temp_data parameter determines whether to look in the temporary data
        storage.

        Parameters:
        ingest_type: str
            String identifier of the database collection to search. This is the same as the type matrix entry for the document type.
        original_source_link: str
            The link to the original source of the document. In reality this is a string that denotes the DAG that ingests the source into the accelerator.
            E.g. "cedar" for the PCOR cedar ingest DAG
        original_source_identifier: str
            The unique identifier associated with the original source. This would be the identifier in the source, such
            as the CEDAR document id
        temp_doc: bool, optional
            Flag indicating whether to search in temporary data storage. Defaults to False.

        Returns:
        dict
            A dictionary representing the document details if found, otherwise None
        """

        db = self.connect_to_db()
        coll = self.build_collection_reference(ingest_type, temp_doc=temp_doc)
        query = {
            "technical_metadata.original_source_link": original_source_link,
            "technical_metadata.original_source_identifier": original_source_identifier,
        }
        doc = coll.find_one(query)
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

    @staticmethod
    def extract_id_from_doc(doc: dict) -> str:
        return str(doc["_id"])

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

                    session.commit_transaction()
                except Exception as e:
                    logger.error(f"Transaction failed: {str(e)}")
                    raise  # Re-raise the exception after logging
