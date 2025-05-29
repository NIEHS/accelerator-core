from accelerator_core.payload import Payload


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

    def to_dict(self) -> dict:
        serialized = {
            "submitter_name": self.submitter_name,
            "submitter_email": self.submitter_email,
            "submit_date": self.submit_date,
            "ingest_type": self.ingest_type,
            "schema_version": self.schema_version,
            "ingest_identifier": self.ingest_identifier,
            "ingest_link": self.ingest_link,
            "ingest_format": self.ingest_format,
            "batch": self.batch,
            "source_metadata_reference_link": self.source_metadata_reference_link,
        }
        return serialized

    @staticmethod
    def from_dict(input_dict: dict):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.submitter_name = input_dict["submitter_name"]
        ingest_source_descriptor.submitter_email = input_dict["submitter_email"]
        ingest_source_descriptor.submit_date = input_dict["submit_date"]
        ingest_source_descriptor.ingest_type = input_dict["ingest_type"]
        ingest_source_descriptor.schema_version = input_dict["schema_version"]
        ingest_source_descriptor.ingest_identifier = input_dict["ingest_identifier"]
        ingest_source_descriptor.ingest_link = input_dict["ingest_link"]
        ingest_source_descriptor.ingest_format = input_dict["ingest_format"]
        ingest_source_descriptor.batch = input_dict["batch"]
        ingest_source_descriptor.source_metadata_reference_link = input_dict[
            "source_metadata_reference_link"
        ]
        return ingest_source_descriptor


class IngestPayload(Payload):

    def __init__(self, ingest_source_descriptor: IngestSourceDescriptor):
        super().__init__(payload=[], payload_path=[], payload_inline=True)
        self.ingest_source_descriptor = ingest_source_descriptor
        self.ingest_successful = True

    def to_dict(self) -> dict:
        serialized = {
            "ingest_source_descriptor": self.ingest_source_descriptor.to_dict(),
            "payload_inline": self.payload_inline,
            "payload_path": self.payload_path,
            "ingest_successful": self.ingest_successful,
            "payload": self.payload,
        }
        return serialized

    @staticmethod
    def from_dict(input_dict: dict):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_source_descriptor = input_dict[
            "ingest_source_descriptor"
        ]
        ingest_source_descriptor.ingest_successful = input_dict["ingest_successful"]
        ingest_source_descriptor.payload_inline = input_dict["payload_inline"]
        ingest_source_descriptor.payload = input_dict["payload"]
        ingest_source_descriptor.payload_path = input_dict["payload_path"]
        return ingest_source_descriptor
