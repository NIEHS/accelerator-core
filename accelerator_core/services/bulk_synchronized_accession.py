"""
Utility parent class for a process that does bulk accession and/or synchronization between an external data
source and an internal catalog.
"""

import logging
from enum import Enum

from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import IngestPayload
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask

logger = logging.getLogger(__name__)


class SynchronizationType(Enum):
    SYNCH_FROM_SOURCE = (
        1  # access each record in the external source and send to the ingest process
    )
    SYNCH_FROM_INTERNAL_MODEL = 2  # access each record in the internal schema and use this to refer back to source


class BulkAccessionSpecification:
    """
    Data describing a bulk accession operation, including the source and the internal target model involved
    """

    def __init__(
        self,
        source_type: str,
        target_schema: str,
        target_schema_version: str,
        synch_type: SynchronizationType,
        temp_data: bool = False,
        additional_parameters=None,
    ):
        """
        Initializes a new instance of the class responsible for handling the conversion
        or mapping from a given source type to a specified target schema and schema
        version. This class allows additional configuration through optional parameters
        and supports enabling or disabling temporary data handling.

        Args:
            source_type: str
                The type of the source data or structure to be mapped.
            target_schema: str
                The schema type of the target to which the source will be converted. This is from the
                type matrix.
            target_schema_version: str
                The version of the target schema being used.
            synch_type: SynchronizationType that describes the behavior of the synchronization process.
            temp_data: bool, optional
                Flag to indicate whether to work with temporary or transient data. Defaults
                to False.
            additional_parameters: dict, optional
                A dictionary of additional configuration parameters. Defaults to None.
        """
        if additional_parameters is None:
            additional_parameters = {}
        self.source_type = source_type
        self.target_type = target_schema
        self.target_schema_version = target_schema_version
        self.synch_type = synch_type
        self.temp_data = temp_data
        self.additional_parameters = additional_parameters


class BulkAccession(AcceleratorWorkflowTask):
    """
    Handles bulk accession of data from an external source, including synchronization with an internal catalog.
    """

    def __init__(
        self,
        accelerator_config: AcceleratorConfig,
        xcom_properties_resolver: XcomPropsResolver,
    ):
        """Initialize Accession with validated data."""
        super().__init__(xcom_properties_resolver)
        self.accelerator_config = accelerator_config

    def bulk_accession(
        self, bulk_accession_specification: BulkAccessionSpecification
    ) -> IngestPayload:
        """
        Handles the initialization of the bulk accession process with the given specification. Note that
        the subclass is responsible for validating the specification and throwing an exception if
        the operation is not supported. E.g. the ingest adapter may not support direct access by
        key to the original source.

        Attributes:
            bulk_accession_specification (BulkAccessionSpecification): The specification
                object required for performing a bulk accession operation.

        Args:
            bulk_accession_specification: The bulk accession configuration that defines
                the parameters for the process.

        Returns:
            IngestPayload: The payload containing the documents selected for dissemination.
        """
        pass
