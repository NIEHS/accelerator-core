import logging

from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomProperties, XcomUtils, XcomPropsResolver
from accelerator_core.workflow.accel_source_ingest import IngestPayload

logger = setup_logger(__name__)

class AcceleratorWorkflowTask():
    """
    Parent class for a workflow task that reads or writes accel data to xcom, also includes helpful
    methods for dealing with context
    """

    def __init__(self, xcomPropertiesResolver:XcomPropsResolver):
        """
        @param: xcomPropertiesResolver XcomPropertiesResolver that can access
        handling configuration
        """
        self.xcomPropertiesResolver = xcomPropertiesResolver
        self.xcomUtils = XcomUtils(xcomPropertiesResolver)

    def report_individual(self, ingest_result: IngestPayload, run_id:str, item_id:str):
        """
        report an individual sub-result.

        This method will:
        * understand how to report the result
        * understand the location to which to write any temp data to pass along
        * keep track of the overall results in IngestResult for close-out

        :param ingest_result: IngestPayload that wraps payload(s). This is passed into this method
        so that the result can be shared across multiple results
        :return: IngestPayload with the result, either in-line or as a temporary file
        """

        if not ingest_result.payload_inline:
            return ingest_result # already in a temp file

        if not self.xcomProperties.temp_files_supported:
            return ingest_result

        logger.info("processing individual result via temp file")
        stored_path = self.xcomUtils.store_dict_in_temp_file(item_id, ingest_result.payload[0],run_id)
        logger.info(f"stored path: {stored_path}")
        







