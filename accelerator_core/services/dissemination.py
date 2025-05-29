"""
Support for retrieving a document from the doc store and passing it along for dissemination.
This built-in can access multiple documents, each of which can be passed along individually for
dissemination.

"""

from accelerator_core.payload import Payload
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import (
    DisseminationDescriptor,
    DisseminationFilter,
    DisseminationPayload,
)
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask


class Dissemination(AcceleratorWorkflowTask):
    """
    Service abstract superclass for disseminating a document from the doc store to an endpoint
    """

    def __init__(
        self,
        accelerator_config: AcceleratorConfig,
        xcom_properties_resolver: XcomPropsResolver,
    ):
        """Initialize Accession with validated data."""
        super().__init__(xcom_properties_resolver)

        self.accelerator_config = accelerator_config

    def disseminate_by_id(
        self, document_id: str, dissemination_request: DisseminationDescriptor
    ) -> DisseminationPayload:
        """
        Disseminate an individual document, identified by its type (parent collection) and its id
        :param document_id: str with unique document id
        :param dissemination_request: DisseminationDescriptor that describes the type, version, and
        other information
        :return: DisseminationPayload with the resulting information
        """
        pass

    def disseminate_by_filter(
        self,
        filter: DisseminationFilter,
        dissemination_request: DisseminationDescriptor,
    ) -> [DisseminationPayload]:
        """
        Apply the given filter to create a set of documents to be disseminated to a target
        :param filter: DisseminationFilter that will select documents to disseminate. The internal meaning
        of the filter is dependent on the particular implementation
        :param dissemination_request: DisseminationRequest that describes the type, version, and other information
        :return: array of documents as DisseminationPayload
        """
        pass
