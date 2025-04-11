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
        self.created = ""
        self.modified = ""
        self.original_source = ""
        self.original_source_link = ""
        self.history = []


class TechnicalMetadataHistory:
    """
    History log entry for technical metadata
    """

    def __init__(self):
        self.timestamp = ""
        self.msg = ""
