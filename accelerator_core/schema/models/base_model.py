from datetime import datetime


class SubmissionInfoModel:
    """
    Represents administrative information about a data source (source, curator info and email)
    """

    def __init__(self):
        self.submitter_comment = ""
        self.submitter_email = ""
        self.submitter_name = ""


class TechnicalMetadataModel:
    """
    Technical metadata about an object
    """

    def __init__(self):
        self.created = ""  # date the original document was created
        self.modified = ""  # date the document was last modified
        self.verified = (
            ""  # date the last verification was done, blank if never verified
        )
        self.target_schema_type = (
            ""  # type_matrix name entry describing the schema of the data kept in accel
        )
        self.target_schema_version = ""  # version of the schema
        self.original_source_identifier = (
            ""  # unique id for the document, will be a pk in accel, can be a doi
        )
        self.original_source_type = (
            ""  # type of data (ingest type) of the original source
        )

        self.original_source_link = (
            ""  # link to document, if available, will be an index in accel
        )
        self.history = []  # TechnicalMetadataHistory
        self.dissemination_endpoints = []  # DisseminationEndpoint


class TechnicalMetadataHistory:
    """
    History log entry for technical metadata
    """

    def __init__(self, timestamp: str, message: str):
        self.timestamp = timestamp
        self.msg = message

    def to_dict(self):
        val = {}
        val["timestamp"] = self.timestamp
        val["msg"] = self.msg
        return val


class DisseminationEndpoint:
    """
    Entry describing an endpoint to which this record has been disseminated
    """

    def __init__(self):
        self.endpoint_type = ""
        self.unique_identifier = ""
        self.link = ""
        self.date = ""

    def to_dict(self):
        val = {}
        val["dissemination_endpoint_type"] = self.endpoint_type
        val["dissemination_unique_identifier"] = self.unique_identifier
        val["dissemination_link"] = self.link
        val["dissemination_date"] = self.date
        return val


def get_time_now_iso():
    now = datetime.now()
    return now.isoformat()


def create_timestamped_log(message: str) -> TechnicalMetadataHistory:
    return TechnicalMetadataHistory(get_time_now_iso(), message)
