from accelerator_core.payload import Payload
from accelerator_core.utils.data_utils import sanitize_boolean


class IngestSourceDescriptor:
    """
    Describes metadata about an ingest source, this includes provenance information as well as technical metadata
    that can be used in downstream processing. This metadata is kept as technical metadata within the archival
    storage
    """

    def __init__(self):
        self.submitter_name = None
        self.submitter_email = None
        self.submit_date = None  # date this ingest identifier runs, should be the launch timestamp of the whole process
        self.ingest_type = None  # maps to ingest type of type matrix
        self.schema_version = None  # version of the specific type
        self.ingest_identifier = None  # run id of the ingest process
        self.ingest_item_id = (
            None  # unique id if this is an individual item, blank for a batch
        )
        self.ingest_link = None  # link to the ingest source
        self.ingest_format = None  # reserved
        self.use_tempfiles = False

    def to_dict(self) -> dict:
        serialized = {
            "submitter_name": self.submitter_name,
            "submitter_email": self.submitter_email,
            "submit_date": self.submit_date,
            "ingest_type": self.ingest_type,
            "ingest_item_id": self.ingest_item_id,
            "schema_version": self.schema_version,
            "ingest_identifier": self.ingest_identifier,
            "ingest_link": self.ingest_link,
            "ingest_format": self.ingest_format,
            "use_tempfiles": self.use_tempfiles,
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
        ingest_source_descriptor.ingest_item_id = input_dict["ingest_item_id"]
        ingest_source_descriptor.ingest_format = input_dict["ingest_format"]
        ingest_source_descriptor.use_tempfiles = sanitize_boolean(
            input_dict["use_tempfiles"]
        )

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
        ingest_source_descriptor = IngestSourceDescriptor.from_dict(
            input_dict["ingest_source_descriptor"]
        )
        ingest_payload = IngestPayload(ingest_source_descriptor)
        ingest_payload.ingest_successful = sanitize_boolean(
            input_dict["ingest_successful"]
        )
        ingest_payload.payload_inline = sanitize_boolean(input_dict["payload_inline"])
        ingest_payload.payload = input_dict["payload"]
        ingest_payload.payload_path = input_dict["payload_path"]
        return ingest_payload


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
    Describes metadata about a data dissemination, this includes provenance information as well as technical metadata
    that can be used in downstream processing.
    """

    def __init__(self):
        self.submitter_name = None
        self.submitter_email = None
        self.submit_date = None
        self.ingest_type = None  # matches type in type matrix
        self.temp_collection = False  # is this in the temp collection
        self.dissemination_type = None  # identifier for the target type
        self.dissemination_version = None  # x.x.x version information for dissemination
        self.dissemination_identifier = None  # run id of the dissemination process
        self.dissemination_item_id = (
            None  # unique id if this is an individual item, blank for a batch
        )

        self.use_tempfiles = False
        self.ingest_identifier = None

    def to_dict(self) -> dict:
        """
        Convert this struct to a dict.
        :return: dict that serializes the descriptor
        """

        serialized = {
            "submitter_name": self.submitter_name,
            "submitter_email": self.submitter_email,
            "submit_date": self.submit_date,
            "ingest_type": self.ingest_type,
            "temp_collection": self.temp_collection,
            "dissemination_type": self.dissemination_type,
            "dissemination_version": self.dissemination_version,
            "dissemination_identifier": self.dissemination_identifier,
            "dissemination_item_id": self.dissemination_item_id,
            "use_tempfiles": self.use_tempfiles,
        }

        return serialized

    def from_dict(self, input_dict: dict):

        dissemination_descriptor = DisseminationDescriptor()
        dissemination_descriptor.submitter_name = input_dict["submitter_name"]
        dissemination_descriptor.submitter_email = input_dict["submitter_email"]
        dissemination_descriptor.submit_date = input_dict["submit_date"]
        dissemination_descriptor.ingest_type = input_dict["ingest_type"]
        dissemination_descriptor.temp_collection = input_dict["temp_collection"]
        dissemination_descriptor.dissemination_type = input_dict["dissemination_type"]
        dissemination_descriptor.dissemination_version = input_dict[
            "dissemination_version"
        ]
        dissemination_descriptor.dissemination_identifier = input_dict[
            "dissemination_identifier"
        ]
        dissemination_descriptor.dissemination_item_id = input_dict[
            "dissemination_item_id"
        ]
        dissemination_descriptor.use_tempfiles = sanitize_boolean(
            input_dict["use_tempfiles"]
        )
        return dissemination_descriptor


class DisseminationPayload(Payload):

    def __init__(self, dissemination_descriptor: DisseminationDescriptor):
        super().__init__(payload=[], payload_path=[], payload_inline=True)
        self.dissemination_descriptor = dissemination_descriptor
        self.dissemination_successful = True

    def to_dict(self) -> dict:
        serialized = {
            "dissemination_descriptor": self.dissemination_descriptor.to_dict(),
            "payload_inline": self.payload_inline,
            "payload_path": [self.payload_path],
            "payload": [self.payload],
            "dissemination_successful": self.dissemination_successful,
        }

        return serialized

    @staticmethod
    def from_dict(input_dict: dict):
        dissemination_payload = DisseminationPayload()
        dissemination_payload.dissemination_descriptor = (
            DisseminationDescriptor.from_dict(input_dict["dissemination_descriptor"])
        )
        dissemination_payload.payload_inline = sanitize_boolean(
            input_dict["payload_inline"]
        )
        dissemination_payload.payload_path = input_dict["payload_path"]
        dissemination_payload.payload = input_dict["payload"]
        dissemination_payload.dissemination_successful = sanitize_boolean(
            input_dict["dissemination_successful"]
        )
        return dissemination_payload
