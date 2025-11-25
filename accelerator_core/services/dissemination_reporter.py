"""
Accounting step updates relevant technical metadata after a dissemination operation
"""

from accelerator_core.schema.models.base_model import DisseminationLinkReport
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask


class DisseminationReporter(AcceleratorWorkflowTask):
    """Handles reporting of operation outcome"""

    def __init__(
        self,
        accelerator_config: AcceleratorConfig,
        xcom_properties_resolver: XcomPropsResolver,
    ):
        """Initialize Accession with validated data."""
        super().__init__(xcom_properties_resolver)
        self.accelerator_config = accelerator_config

    def report_dissemination_result(
        self, dissemination_link_report: DisseminationLinkReport
    ):
        """
        After accessioning a record to a dissemination endpoint, this task can recive the report
        of the endpoint operation and link the dissemination endpoint to the accelerator model record.

        The input DisseminationLinkReport is the output of the dissemination service and can contain
        a success flag and error message. This task should consult before attempting the link.

        The DisseminationLinkReport should contain information to identify the accel record along with (hopefully)
        information that could identify the location of the dissemination. In an ideal case
        one should be able to go from accelerator to the actual location, but there may be cases
        where only partial information is possible, so we do the best we can.

        @param dissemination_link_report:DisseminationLinkReport with the output of the dissemination
        attempt
        """
        pass
