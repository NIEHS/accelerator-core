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


class DisseminationDescriptor:
    """
    Describes metadata about adata dissemination, this includes provenance information as well as technical metadata
    that can be used in downstream processing.
    """

    def __init__(self):
        self.submitter_name = None
        self.submitter_email = None
        self.submit_date = None
        self.ingest_type = None  # matches type in type matrix
        self.temp_collection = False  # is this in the temp collection
        self.inline_results = (
            True  # request the data be passed inline in the DisseminationResult
        )
        self.dissemination_type = None  # identifier for the target type
        self.dissemination_version = None  # x.x.x version information for dissemination


class DisseminationPayload:
    """
    Response from a dissemination request
    """

    def __init__(self, dissemination_request: DisseminationDescriptor):
        self.dissemination_request = dissemination_request
        self.dissemination_successful = True
        self.payload_inline = True
        self.payload = None
        self.payload_path = None


class Dissemination:
    """
    Service abstract superclass for disseminating a document from the doc store to an endpoint
    """

    def __init__(self, accelerator_config: AcceleratorConfig):
        """Initialize Accession with validated data."""
        self.accelerator_config = accelerator_config

    def disseminate_by_id(
        self, document_id: str, dissemination_request: DisseminationDescriptor
    ) -> DisseminationPayload:
        """
        Disseminate an individual document, identified by its type (parent collection) and its id
        :param document_id: str with unique document id
        :param dissemination_request: DisseminationDescriptor that describes the type, version, and
        other information
        :return: DisseminationPayload with the resulting information
        """
        pass

    def disseminate_by_filter(
        self,
        filter: DisseminationFilter,
        dissemination_request: DisseminationDescriptor,
    ) -> [DisseminationPayload]:
        """
        Apply the given filter to create a set of documents to be disseminated to a target
        :param filter: DisseminationFilter that will select documents to disseminate. The internal meaning
        of the filter is dependent on the particular implementation
        :param dissemination_request: DisseminationRequest that describes the type, version, and other information
        :return: array of documents as DisseminationPayload
        """
        pass
