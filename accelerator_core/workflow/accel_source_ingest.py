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
        self.schema_version = None
        self.ingest_identifier = None
        self.ingest_link = None
        self.ingest_format = None
        self.batch = False
        self.source_metadata_reference_link = None


class IngestPayload:

    def __init__(self, ingest_source_descriptor: IngestSourceDescriptor):
        self.ingest_source_descriptor = ingest_source_descriptor
        self.source_document_detail = None
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

    def ingest(self, additional_parameters: dict) -> IngestPayload:
        """
        primary method for subclasses to implement, this is the actual ingest, which means accessing the target
        data source and returning a result that includes provenance and technical metadata, along with a payload that
        is either the serialized result or a path or locator that can be used to extract the result.
        :param additional_parameters: dict of individual parameters that can be fed to this method per implementation
        :return: IngestPayload that wraps payload(s) with additional metadata
        """
        pass

    def ingest_single(self, identifier, additional_parameters: dict) -> IngestPayload:
        """
        proposed (WIP) method to support background access/update of accel data by checking the registered data/document
        on the original source
        TODO: utilize for verification and update callbacks in maintenance workflows, update logs
        :param identifier: identifier from the accel record that allows re-access on the target site
        :param additional_parameters: dict of individual parameters that can be fed to this method per implementation
        :return: IngestPayload that wraps payload(s) with additional metadata
        """
        pass

    def report_individual(self, ingest_result: IngestPayload):
        """
        report an individual sub-result. (WIP).
        TODO: based on in-mem or by temp file, preserve the result for a single object

        This method will:
        * understand how to report the result
        * understand the location to which to write any temp data to pass along
        * keep track of the overall results in IngestResult for close-out

        :param ingest_result: IngestPayload that wraps payload(s). This is passed into this method
        so that the result can be shared across multiple results
        :return: None
        """
        pass

    def close_out(self, ingest_result: IngestPayload):
        """
        Close out an ingest when all individual reports are done, do any cleanup
        TODO: consider writing out a manifest if this is a bulk action
        :param ingest_result: IngestPayload that wraps payload(s). This is passed into this method as a shared object
        :return: None
        """
        pass
