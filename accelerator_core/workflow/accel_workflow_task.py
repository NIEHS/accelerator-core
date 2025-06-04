import logging

from accelerator_core.payload import Payload
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import (
    XcomProperties,
    XcomUtils,
    XcomPropsResolver,
)
from accelerator_core.workflow.accel_data_models import (
    IngestPayload,
    DisseminationPayload,
)

logger = setup_logger(__name__)


class AcceleratorWorkflowTask:
    """
    Parent class for a workflow task that reads or writes accel data to xcom, also includes helpful
    methods for dealing with context
    """

    def __init__(self, xcom_properties_resolver: XcomPropsResolver):
        """
        @param: xcom_properties_resolver XcomPropertiesResolver that can access
        handling configuration
        """
        self.xcom_properties_resolver = xcom_properties_resolver
        self.xcomUtils = XcomUtils(xcom_properties_resolver)

    def payload_resolve(self, payload: Payload, index: int) -> dict:
        """
        Callback function that will yield a payload that has been resolved (meaning
        the values in the payload have been marshaled from xcom into a dict). This handles
        cases where the payload was stored in a temporary location.
        :param payload: Payload
        :param index: index of the payload to resolve
        :return: dict with the resolved payload data
        """
        logger.info(f"payload resolve for payload {payload}")
        if payload.payload_inline:
            if index < len(payload.payload):
                logger.debug("inline payload returned")
                return payload.payload[index]
            else:
                raise Exception("payload index out of range")

        if index < len(payload.payload_path):
            mypath = payload.payload_path[index]
            logger.info(f"payload path returned, resolving {mypath}")
            return self.xcomUtils.retrieve_dict_from_temp_file(mypath)
        else:
            raise Exception("payload path index out of range")

    def report_individual(self, ingest_result: IngestPayload, item_id: str, item: dict):
        """
        report an individual sub-result.

        This method will:
        * understand how to report the result
        * understand the location to which to write any temp data to pass along
        * keep track of the overall results in IngestResult for close-out

        @param: ingest_result IngestPayload that will receive the new item, NB that the run_id should
            be provided in the IngestSourceDescriptor that is part of the payload
        @param: item_id string that identifies the item to report
        @param: item dict that contains information about the item to report
        @return: None (IngestPayload will have the item appended in the correct fashion)

        """
        logger.info("report individual for item %s", item_id)

        if not ingest_result.ingest_source_descriptor.ingest_identifier:
            raise Exception(
                "no ingest_identifier (run_id) provided in source descriptor"
            )

        if not item_id:
            raise Exception("no item_id provided")

        ingest_result.ingest_source_descriptor.ingest_item_id = item_id

        if not ingest_result.ingest_source_descriptor.use_tempfiles:
            logger.info("appending the item inline")
            ingest_result.payload.append(item)
            ingest_result.payload_inline = True
            return

        logger.info("processing individual result via temp file")
        stored_path = self.xcomUtils.store_dict_in_temp_file(
            item_id, item, ingest_result.ingest_source_descriptor.ingest_identifier
        )
        logger.info(f"stored path: {stored_path}")
        ingest_result.payload_path.append(stored_path)
        ingest_result.payload_inline = False

    def get_payload_length(self, payload: Payload) -> int:
        """
        Get the number of elements in a payload whether inline or via temp file
        @param: payload Payload that will receive the new item
        @return: int with the length of the payload
        """
        if payload.payload_inline:
            return len(payload.payload)
        else:
            return len(payload.payload_path)

    def report_individual_dissemination(
        self, dissemination_payload: DisseminationPayload, item_id: str, item: dict
    ):
        """
        report an individual sub-result.

        This method will:
        * understand how to report the result
        * understand the location to which to write any temp data to pass along
        * keep track of the overall results in DisseminationPayload for close-out

        @param: dissemination_payload DisseminationPayload that will receive the new item, NB that the run_id should
            be provided in the DisseminationDescriptor that is part of the payload
        @param: item_id string that identifies the item to report
        @param: item dict that contains information about the item to report
        @return: None (DisseminationPayload will have the item appended in the correct fashion)

        """

        if not dissemination_payload.dissemination_descriptor.dissemination_identifier:
            raise Exception(
                "no dissemination_identifier (run_id) provided in descriptor"
            )

        if not item_id:
            raise Exception("no item_id provided")

        dissemination_payload.dissemination_descriptor.dissemination_item_id = item_id

        if not dissemination_payload.dissemination_descriptor.use_tempfiles:
            logger.debug("appending the item inline")
            dissemination_payload.payload.append(item)
            dissemination_payload.payload_inline = True
            return

        logger.info("processing individual result via temp file")
        stored_path = self.xcomUtils.store_dict_in_temp_file(
            item_id,
            item,
            dissemination_payload.dissemination_descriptor.dissemination_identifier,
        )
        logger.info(f"stored path: {stored_path}")
        dissemination_payload.payload_path.append(stored_path)
        dissemination_payload.payload_inline = True
