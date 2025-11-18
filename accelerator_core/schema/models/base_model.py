from datetime import datetime


class SubmissionInfoModel:
    """
    Represents administrative information about a data source (source, curator info and email)
    """

    def __init__(self):
        self.submitter_comment = ""
        self.submitter_email = ""
        self.submitter_name = ""

    def to_dict(self):
        val = {}
        val["submitter_comment"] = self.submitter_comment
        val["submitter_email"] = self.submitter_email
        val["submitter_name"] = self.submitter_name
        return val

    @staticmethod
    def from_dict(dict_obj):
        obj = SubmissionInfoModel()
        obj.submitter_comment = dict_obj["submitter_comment"]
        obj.submitter_email = dict_obj["submitter_email"]
        obj.submitter_name = dict_obj["submitter_name"]
        return obj


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
            ""  # unique id for the document, will be a accel database id
            # (e.g. a mongo _id)
        )
        self.original_source_type = (
            ""  # type of data (ingest type) of the original source
        )

        self.original_source_link = (
            ""  # link to document, if available, will be an index in accel
        )
        self.history = []  # TechnicalMetadataHistory
        self.dissemination_endpoints = []  # DisseminationEndpoint

    def to_dict(self):
        val = {}
        val["created"] = self.created
        val["modified"] = self.modified
        val["verified"] = self.verified
        val["target_schema_type"] = self.target_schema_type
        val["target_schema_version"] = self.target_schema_version
        val["original_source_identifier"] = self.original_source_identifier
        val["original_source_type"] = self.original_source_type
        val["original_source_link"] = self.original_source_link
        val["history"] = [h.to_dict() for h in self.history]
        val["dissemination_endpoints"] = [
            d.to_dict() for d in self.dissemination_endpoints
        ]
        return val

    @staticmethod
    def from_dict(dict_obj):
        obj = TechnicalMetadataModel()
        obj.created = dict_obj["created"]
        obj.modified = dict_obj["modified"]
        obj.verified = dict_obj["verified"]
        obj.target_schema_type = dict_obj["target_schema_type"]
        obj.target_schema_version = dict_obj["target_schema_version"]
        obj.original_source_identifier = dict_obj["original_source_identifier"]
        obj.original_source_type = dict_obj["original_source_type"]


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

    @staticmethod
    def from_dict(dict_obj):
        obj = TechnicalMetadataHistory(dict_obj["timestamp"], dict_obj["msg"])
        return obj


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

    @staticmethod
    def from_dict(dict_obj):
        obj = DisseminationEndpoint()
        obj.endpoint_type = dict_obj["dissemination_endpoint_type"]
        obj.unique_identifier = dict_obj["dissemination_unique_identifier"]
        obj.link = dict_obj["dissemination_link"]
        obj.date = dict_obj["dissemination_date"]
        return obj


class DisseminationLinkReport:
    """
    Contains information that can link a particular dissemination of a model to a specific endpoint. This is used
    in DAGS to report a successful dissemination.
    """

    def __init__(self):

        self.target_schema_type = (
            ""  # type_matrix name entry describing the schema of the data kept in accel
        )
        self.target_schema_version = ""  # version of the schema
        self.temporary_data = (
            False  # indicates whether this is kept as temporary data in accel
        )
        self.original_source_identifier = (
            ""  # unique id for the document in the accel database
        )
        self.original_source_type = (
            ""  # type of data (ingest type) of the original source
        )
        self.success = True
        self.message = ""
        self.dissemination_endpoint = None  # DisseminationEndpoint

    @staticmethod
    def from_dict(dict_obj):
        obj = DisseminationLinkReport()
        obj.target_schema_type = dict_obj["target_schema_type"]
        obj.target_schema_version = dict_obj["target_schema_version"]
        obj.original_source_identifier = dict_obj["original_source_identifier"]
        obj.original_source_type = dict_obj["original_source_type"]
        obj.temporary_data = dict_obj.get("temporary_data", False)
        obj.success = dict_obj.get("success", True)
        obj.message = dict_obj.get("message", "")
        obj.dissemination_endpoint = DisseminationEndpoint.from_dict(
            dict_obj["dissemination_endpoint"]
        )
        return obj

    @staticmethod
    def to_dict(obj):
        return {
            "target_schema_type": obj.target_schema_type,
            "target_schema_version": obj.target_schema_version,
            "original_source_identifier": obj.original_source_identifier,
            "original_source_type": obj.original_source_type,
            "temporary_data": obj.temporary_data,
            "success": obj.success,
            "message": obj.message,
            "dissemination_endpoint": DisseminationEndpoint.to_dict(
                obj.dissemination_endpoint
            ),
        }


def get_time_now_iso():
    now = datetime.now()
    return now.isoformat()


def create_timestamped_log(message: str) -> TechnicalMetadataHistory:
    return TechnicalMetadataHistory(get_time_now_iso(), message)
