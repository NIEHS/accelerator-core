"""
Services for the AIP store, this includes data access and CRUD operations for metadata documents
This is the base class for all AIP stores, actual persistenced defined in subclass. Can be mocked for
testing.
"""


class AIPStore:
    """
    Defines an AIP service layer
    """

    def __init__(self):
        pass

    def verify_connect(self) -> bool:
        """
        Verify that the service can connect to a running AIP store
        :return: bool of True if can connect, False otherwise
        """
        pass

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
