from abc import ABC, abstractmethod

from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload
from accelerator_core.workflow.accel_source_ingest import (
    IngestSourceDescriptor,
    IngestPayload,
)
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask


class DisseminationCrosswalk(AcceleratorWorkflowTask):
    """Abstract superclass for mapping raw data to a structured JSON format."""

    def __init__(self, xcom_props_resolver: XcomPropsResolver):
        """
        @param: xcom_properties_resolver XcomPropertiesResolver that can access
        handling configuration
        """

        super().__init__(xcom_props_resolver)

    @abstractmethod
    def transform(
        self, dissemination_payload: DisseminationPayload
    ) -> DisseminationPayload:
        """Convert raw data into a standardized format.
        :param ingest_result: The ingest result.
        :return revised DisseminationPayload with the crosswalked document in payload

        """

        pass
