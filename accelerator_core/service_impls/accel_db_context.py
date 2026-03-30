from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.mongo_tools import initialize_mongo_client

"""
Context object passed to services, wraps the db connections
"""


class AccelDbContext(object):
    """
    Database context for services, wraps the db connections
    """

    def __init__(self, accelerator_config: AcceleratorConfig):
        self.accelerator_config = accelerator_config
        self.mongo_client = initialize_mongo_client(self.accelerator_config)
        self.db = self.mongo_client.get_database(
            self.accelerator_config.params["mongo.db.name"]
        )

    def start_session(self):
        return self.db.client.start_session()

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
