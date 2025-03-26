"""
Support for retrieving a document from the doc store and passing it along for dissemination.
This built-in can access multiple documents, each of which can be passed along individually for
dissemination.

"""

from accelerator_core.utils.accelerator_config import AcceleratorConfig


class DisseminationFilter:
    """
    Filter for objects in the Accel data store to be passed along for dissemination
    """

    def filter(self, filter_terms: dict):
        """
        Filter requests (that will be targeted to a chosen collection based on the context) to deliver for
        dissemination
        :param filter_terms: dict with filtering terms
        """


class DisseminationRequest:
    """
    Describes metadata about adata dissemination, this includes provenance information as well as technical metadata
    that can be used in downstream processing.
    """

    def __init__(self):
        self.submitter_name = None
        self.submitter_email = None
        self.submit_date = None
        self.ingest_type = None
        self.temp_collection = False
        self.inline_results = True
        self.destination = None


class DisseminationResult:
    """
    Response from a dissemination request
    """

    def __init__(self, dissemination_request: DisseminationRequest):
        self.dissemination_request = dissemination_request
        self.dissemination_successful = True
        self.batch = False
        self.payload_inline = True
        self.payload = []
        self.payload_path = []


class Dissemination:
    """
    Service abstract superclass for disseminating a document from the doc store to an endpoint
    """

    def __init__(self, accelerator_config: AcceleratorConfig):
        """Initialize Accession with validated data."""
        self.accelerator_config = accelerator_config

    def disseminate_by_id(
        self, document_id: str, dissemination_request: DisseminationRequest
    ) -> DisseminationResult:
        """
        Disseminate an individual document, identified by its type (parent collection) and its id
        :param document_id: str with unique document id
        :param dissemination_specification: DisseminationSpecification that describes the type, version, and
        other information
        :return: DisseminationResult with the resulting information.
        """

    def disseminate_by_filter(
        self, filter: DisseminationFilter, dissemination_request: DisseminationRequest
    ) -> DisseminationResult:
        """
        Apply the given filter to create a set of documents to be disseminated to a target
        :param document_filter: DisseminationFilter that will select documents to disseminate
        :return: array of documents as json
        """
