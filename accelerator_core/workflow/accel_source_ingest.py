"""
Superclass for an ingest component
"""

from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomProperties, XcomPropsResolver
from accelerator_core.workflow.accel_data_models import (
    IngestSourceDescriptor,
    IngestPayload,
)
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask

logger = setup_logger("accelerator")


class AccelIngestComponent(AcceleratorWorkflowTask):
    """
    Abstract parent class for ingest components, this accesses a target
    """

    def __init__(
        self,
        ingest_source_descriptor: IngestSourceDescriptor,
        xcom_props_resolver: XcomPropsResolver,
    ):
        """
        Describes the type of ingest, the submitter, the source and other provenance information.
        Subclasses may introduce other configuration, including secrets and parameters for accessing the
        target source
        :param ingest_source_descriptor: IngestSourceDescriptor with submission information
        :param xcom_properties: XcomProperties with information about data handling
        """
        super().__init__(xcom_props_resolver)
        self.ingest_source_descriptor = ingest_source_descriptor

    def reacquire_supported(self) -> bool:
        """
        Informational method that indicates whether this ingest component supports reacquisition
        """
        return False

    def reacquire(self, ingest_id, additional_parameters: dict) -> IngestPayload:
        """
        PROPOSED

        Method to reacquire an individual document from the original source. This allows the system to
        validate or update data in accelerator by returning to the original source.
        :param ingest_id: unique identifier of the item at the source
        :param additional_parameters: dict of individual parameters that can be fed to this method per implementation

        """
        pass

    def ingest(self, additional_parameters: dict) -> IngestPayload:
        """
        primary method for subclasses to implement, this is the actual ingest, which means accessing the target
        data source and returning a result that includes provenance and technical metadata, along with a payload that
        is either the serialized result or a path or locator that can be used to extract the result.
        :param additional_parameters: dict of individual parameters that can be fed to this method per implementation
        :return: IngestPayload that wraps payload(s) with additional metadata

        Note that the IngestSourceDescriptor has an ingest_identifier that should be set to the run_id of the workflow
        or other representation of the process that is calling this task

        """
        pass

    def ingest_single(self, identifier, additional_parameters: dict) -> IngestPayload:
        """
        proposed (WIP) method to support background access/update of accel data by checking the registered data/document
        on the original source
        :param identifier: identifier from the accel record that allows re-access on the target site
        :param additional_parameters: dict of individual parameters that can be fed to this method per implementation
        :return: IngestPayload that wraps payload(s) with additional metadata

        Note that the IngestSourceDescriptor has an ingest_identifier that should be set to the run_id of the workflow
        or other representation of the process that is calling this task. The resulting ingestPayload will carry
        that source descriptor and, if using the 'report' methods provided, will ingest the individual item identifier
        into each item produced


        """
        pass
