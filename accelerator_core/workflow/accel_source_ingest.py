"""
Superclass for an ingest component
"""


class IngestSourceDescriptor:
    """
    Describes metadata about an ingest source, this includes provenance information as well as technical metadata
    that can be used in downstream processing. This metadata is kept as technical metadata within the archival
    storage
    """

    def __init__(self):
        self.submitter_name = None
        self.submitter_email = None
        self.submit_date = None
        self.ingest_type = None
        self.type = None
        self.schema_version = None
        self.ingest_identifier = None
        self.ingest_link = None
        self.ingest_format = None
        self.batch = False


class IngestResult:

    def __init__(self, ingest_source_descriptor: IngestSourceDescriptor):
        self.ingest_source_descriptor = ingest_source_descriptor
        self.ingest_successful = True
        self.payload_inline = True
        self.payload = []
        self.payload_path = []


class AccelIngestComponent:
    """
    Abstract parent class for ingest components, this accesses a target
    """

    def __init__(self, ingest_source_descriptor: IngestSourceDescriptor):
        """
        Describes the type of ingest, the submitter, the source and other provenance information.
        Subclasses may introduce other configuration, including secrets and parameters for accessing the
        target source
        :param ingest_source_descriptor: IngestSourceDescriptor with submission information
        """
        self.ingest_source_descriptor = ingest_source_descriptor

    def ingest(self, additional_parameters: dict) -> IngestResult:
        """
        primary method for subclasses to implement, this is the actual ingest, which means accessing the target
        data source and returning a result that includes provenance and technical metadata, along with a payload that
        is either the serialized result or a path or locator that can be used to extract the result.
        :param additional_parameters: dict of individual parameters that can be fed to this method per implementation
        :return: IngestResult that wraps payload(s) with additional metadata
        """
        pass
