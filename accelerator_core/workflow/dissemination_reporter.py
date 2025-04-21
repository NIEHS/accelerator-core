"""
Post-dissemination reporter and logger
"""

from accelerator_core.services.dissemination import DisseminationDescriptor
from accelerator_core.utils.accelerator_config import AcceleratorConfig


class DisseminationReporter:
    """
    Service abstract superclass for accounting and reporting of a dissemination action
    """

    def __init__(self, accelerator_config: AcceleratorConfig):
        """Initialize Accession with validated data."""
        self.accelerator_config = accelerator_config

    def report_dissemination_result(
        self, document_id: str, dissemination_descriptor: DisseminationDescriptor
    ):
        """
        reporting callback for dissemination result, can update the accel database with the result and any
        other logging/reporting
        :param document_id: unique document id in accel
        :param dissemination_descriptor: DisseminationDescriptor with information about the dissemination attempt and
        any associated logs
        """
        pass
