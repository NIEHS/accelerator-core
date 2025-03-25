"""
Support for retrieving a document from the doc store and passing it along for dissemination.
This built-in can access multiple documents, each of which can be passed along individually for
dissemination.

"""

from accelerator_core.utils.accelerator_config import AcceleratorConfig


class DisseminationSpecification:
    """
    Represents a dissemination of data from the doc store to an endpoint
    """

    def __init__(self):
        self.dissemination_target_type = ""
        self.dissemination_target_version = ""
        self.submitter_name = None
        self.submitter_email = None
        self.submit_date = None
        self.ingest_type = None
        self.schema_version = None


class DisseminationFilter:
    """
    Filter to be applied to content within the doc store to derive a set of documents
    to send down the dissemination pipeline
    """

    def filter(self, parameters: dict) -> []:
        """
        Execute the filter and produce a set of documents that match the filter
        :param parameters: arbitrary filter parameters to tune the filter
        :return: array of json documents that match the filter
        """


class Dissemination:
    """
    Service abstract superclass for disseminating a document from the doc store to an endpoint
    """

    def __init__(self, accelerator_config: AcceleratorConfig):
        """Initialize Accession with validated data."""
        self.accelerator_config = accelerator_config

    def disseminate_by_id(
        self, document_id: str, dissemination_specification: DisseminationSpecification
    ) -> dict:
        """
        Disseminate an individual document, identified by its type (parent collection) and its id
        :param document_id: str with unique document id
        :param dissemination_specification: DisseminationSpecification that describes the type, version, and
        other information
        :return: dict with the document information
        """

    def disseminate_by_filter(self, document_filter: DisseminationFilter) -> []:
        """
        Apply the given filter to create a set of documents to be disseminated to a target
        :param document_filter: DisseminationFilter that will select documents to disseminate
        :return: array of documents as json
        """
