"""
Superclass for an ingest component
"""

import logging

from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import (
    IngestSourceDescriptor,
    IngestPayload,
    SynchType,
)
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask

logger = logging.getLogger(__name__)


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

    def synch(
        self, synch_type: SynchType, identifier: str, additional_parameters: dict
    ) -> IngestPayload:
        """
        primary method for subclasses to implement, this is the actual ingest, which means accessing the target
        data source and returning a result that includes provenance and technical metadata, along with a payload that
        is either the serialized result or a path or locator that can be used to extract the result.
        :param additional_parameters: dict of individual parameters that can be fed to this method per implementation
        :param identifier: str with the identifier of the source of data on the target site
        :param synch_type: str with the type of synch to perform
        :return: IngestPayload that wraps payload(s) with additional metadata

        Note that the IngestSourceDescriptor has an ingest_identifier that should be set to the run_id of the workflow
        or other representation of the process that is calling this task

        This method is meant to cover ingest of one or many, based on unique parameters that are put into the additional_parameters
        field. The ingest_single() method below is specifically meant to obtain one data record via the unique identifer
        parameter (which can be a url, doi, guid, or other unique identifier that can tie the archived version back
        to the original source.

        Implementors can advertise the ability to link back to the original source via this identifier by
        implementing the reacquire_supported method, returning true in that case.

        """
        pass

    def ingest_single(self, identifier, additional_parameters: dict) -> IngestPayload:
        """
        Method to support background access/update of accel data by checking the registered data/document
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
