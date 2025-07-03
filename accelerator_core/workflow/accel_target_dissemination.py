"""
Adapter that takes formatted data (disseminated and transformed for the target)
"""

from accelerator_core.services.dissemination import DisseminationPayload
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask


class AccelDisseminationComponent(AcceleratorWorkflowTask):
    """
    Abstract parent class for dissemination components, this pushes data to a target
    """

    def __init__(self, xcom_props_resolver: XcomPropsResolver):
        """
        @param: xcom_properties_resolver XcomPropertiesResolver that can access
        handling configuration
        """

        super().__init__(xcom_props_resolver)

    def disseminate(
        self, dissemination_payload: DisseminationPayload, additional_parameters: dict
    ) -> DisseminationPayload:
        """
        absract method to be implemented per dissemination target. This takes a DisseminationPayload with
        inline data or path to temporary data and should handle data dissemination to some target. It will return
        a structure that can be used downstream to update the technical metadata log about the dissemination
        :param dissemination_payload: DisseminationPayload with the dissemination data
        :param additional_parameters: dict with additional parameters unique to a target
        :return: DisseminationPayload with results and additional logging on success/failure of a dissemination
        """

        # TODO: check for duplicate
        # TODO: add update method or flag?
        # tech metadata should capture the location where this guy was disseminated, should this be a new array of
        # disseminated location records in tech metadata?
        # also a status flag? e.g. validated, missing at source
        pass
