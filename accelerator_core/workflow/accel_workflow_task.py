import logging

from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomProperties, XcomUtils, XcomPropsResolver
from accelerator_core.workflow.accel_data_models import IngestPayload

logger = setup_logger(__name__)

class AcceleratorWorkflowTask():
    """
    Parent class for a workflow task that reads or writes accel data to xcom, also includes helpful
    methods for dealing with context
    """

    def __init__(self, xcom_properties_resolver:XcomPropsResolver):
        """
        @param: xcom_properties_resolver XcomPropertiesResolver that can access
        handling configuration
        """
        self.xcom_properties_resolver = xcom_properties_resolver
        self.xcomUtils = XcomUtils(xcom_properties_resolver)

    def report_individual(self, ingest_result: IngestPayload, run_id:str, item_id:str, item:dict):
        """
        report an individual sub-result.

        This method will:
        * understand how to report the result
        * understand the location to which to write any temp data to pass along
        * keep track of the overall results in IngestResult for close-out

        @param: ingest_result IngestPayload that will receive the new item
        @param: run_id string that identifies the workflow run
        @param: item_id string that identifies the item to report
        @param: item dict that contains information about the item to report
        @return: None (IngestPayload will have the item appended in the correct fashion)

        """

        if ingest_result.payload_inline:
            logger.debug("appending the item inline")
            ingest_result.payload.append(item)
            return

        logger.info("processing individual result via temp file")
        stored_path = self.xcomUtils.store_dict_in_temp_file(item_id,item,run_id)
        logger.info(f"stored path: {stored_path}")
        ingest_result.payload_path.append(stored_path)








