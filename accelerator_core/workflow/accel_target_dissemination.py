"""
Adapter that takes formatted data (disseminated and transformed for the target)
"""

from accelerator_core.services.dissemination import DisseminationPayload


class AccelDisseminationComponent:
    """
    Abstract parent class for ingest components, this accesses a target
    """

    def __init__(self):
        pass

    def disseminate(
        self, dissemination_request: DisseminationPayload, additional_parameters: dict
    ):
        """
        primary method for subclasses to implement, this is the actual ingest, which means accessing the target
        data source and returning a result that includes provenance and technical metadata, along with a payload that
        is either the serialized result or a path or locator that can be used to extract the result.
        :param additional_parameters: dict of individual parameters that can be fed to this method per implementation
        :return: IngestResult that wraps payload(s) with additional metadata
        """
        pass
