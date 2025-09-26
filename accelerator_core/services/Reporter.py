"""
Accounting step updates relevant technical metadata after an operation
"""

from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask


class Reporter(AcceleratorWorkflowTask):
    """Handles reporting of operation outcome"""

    def __init__(
        self,
        accelerator_config: AcceleratorConfig,
        xcom_properties_resolver: XcomPropsResolver,
    ):
        """Initialize Accession with validated data."""
        super().__init__(xcom_properties_resolver)
        self.accelerator_config = accelerator_config
