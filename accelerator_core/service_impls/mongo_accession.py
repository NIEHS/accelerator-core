"""
Accession support concrete implementation for Mongo data store
"""

from bson import ObjectId

from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.services.accession import Accession
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.mongo_tools import initialize_mongo_client
from accelerator_core.utils.schema_tools import CURRENT_ACCEL_SCHEMA_VERSION
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.schema_tools import validate_json_against_schema

logger = setup_logger("accelerator")


class AccessionMongo(Accession):
    """
    Accession module based on Mongo persistence
    """

    def __init__(
        self, acclerator_config: AcceleratorConfig, accel_db_context: AccelDbContext
    ):
        """
        Initialize the Accession sservice
        :param acclerator_config: AcceleratorConfig with general configuration
        :param accel_db_context: AccelDbContext that holds the db connection
        """
        Accession.__init__(self, acclerator_config)
        self.accel_db_context = accel_db_context

    def validate(
        self, json_dict: dict, schema_version: str = CURRENT_ACCEL_SCHEMA_VERSION
    ) -> bool:
        return super().validate(json_dict, schema_version)

    def ingest(
        self,
        acel_document: dict,
        check_duplicates: bool = True,
        temp_doc: bool = False,
        schema_version: str = CURRENT_ACCEL_SCHEMA_VERSION,
    ) -> str:
        """
        Ingest the given document
        :param acel_document: dict which is the document structure
        :param check_duplicates: bool indicates whether pre-checks for duplicate data run
        :param temp_doc: bool indicates whether the document is temporary or not
        :param schema_version: str schema version for Accelerator
        :return: str with id of the ingested document
        """
        logger.info("ingest()")
        valid = self.validate(acel_document, schema_version)
        if not valid:
            raise Exception("Invalid document provided")

        db = self.connect_to_db()
        coll = self.build_column_reference(db, temp_doc)

        id = coll.insert_one(acel_document).inserted_id

        logger.info(f"inserted id {id}")
        return id

    def decommission(self, document_id):
        """
        Remove the doc from the AIP store, this is not for temporary docs
        :param document_id: unique id for the document
        """
        logger.info(f"decommision({document_id})")

        db = self.connect_to_db()
        coll = self.build_column_reference(db, False)

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

        logger.info(f"find_by_id({document_id}) is temp doc? {temp_doc}")

        db = self.connect_to_db()
        coll = self.build_column_reference(db, False)
        doc = coll.find_one({"_id": ObjectId(document_id)})
        return doc

    def connect_to_db(self):
        return self.accel_db_context.db

    def build_column_reference(self, db, temp_doc: bool = False):
        if temp_doc:
            coll_name = self.accelerator_config.properties["mongo.temp.collection"]
        else:
            coll_name = self.accelerator_config.properties["mongo.aip.collection"]

        return db[coll_name]
