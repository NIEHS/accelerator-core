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
    ) -> DisseminationPayload:
        """
        absract method to be implemented per dissemination target. This takes a DisseminationPayload with
        inline data or path to temporary data and should handle data dissemination to some target. It will return
        a structure that can be used downstream to update the technical metadata log about the dissemination
        :param dissemination_request: DisseminationPayload with the dissemination data
        :param additional_parameters: dict with additional parameters unique to a target
        :return: DisseminationPayload with results and additional logging on success/failure of a dissemination
        """
        pass
