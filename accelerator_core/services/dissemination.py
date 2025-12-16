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
        @param document_id: str with unique document id
        @param dissemination_request: DisseminationDescriptor that describes the type, version, and
        other information
        @return: DisseminationPayload with the resulting information
        """
        pass

    def disseminate_by_original_source_and_id(
        self,
        original_source: str,
        original_document_identifier,
        dissemination_request: DisseminationDescriptor,
    ) -> DisseminationPayload:
        """
        Apply a filter to create and disseminate a single document specified target.

        This method is used for creating a dissemination payload by applying a filter
        that selects specific documents. The filtering mechanism is determined by the
        implementation and works on provided source and document identifiers. This is meant to return a single
        document based on its original source (e.g. "cedar") and the original identifier (e.g. the document DOI in cedar).

        This is distinguised from the dissemination_by_id method which is meant to return a single document based on its
        accelerator database identifier.

        Parameters:
            original_source: str
                The source where the original document resides. This represents the DAG that ingested the document
                originally
            original_document_identifier
                The identifier of the document in the original source. (e.g. the CEDAR generated document GUID).
            dissemination_request: DisseminationDescriptor
                A descriptor that details the dissemination type, version, and
                additional relevant information.

        Returns:
            DisseminationPayload
                The payload containing the documents selected for dissemination.
        """
        pass

    def disseminate_by_filter(
        self,
        filter: DisseminationFilter,
        dissemination_request: DisseminationDescriptor,
    ) -> [DisseminationPayload]:
        """
        Apply the given filter to create a set of documents to be disseminated to a target
        @param filter: DisseminationFilter that will select documents to disseminate. The internal meaning
        of the filter is dependent on the particular implementation
        @param dissemination_request: DisseminationRequest that describes the type, version, and other information
        @return: array of documents as DisseminationPayload
        """
        pass
