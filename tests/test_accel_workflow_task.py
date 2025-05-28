import os
import shutil
import unittest

from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_source_ingest import IngestPayload, IngestSourceDescriptor
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask


class TestAcceleratorWorkflowTask(unittest.TestCase):
    def test_serialize_inline(self):
        temp_dirs_path = "test_resources/temp_dirs"
        runid = "test_serialize_file"
        file_key = "mykey"
        path = os.path.join(temp_dirs_path, runid)

        if os.path.exists(path):
            shutil.rmtree(path)

        my_vals = {"mykey": "myvalue"}
        xcom_props_resolver = DirectXcomPropsResolver(temp_files_supported=True, temp_files_location=temp_dirs_path)

        ingestSourceDescriptor = IngestSourceDescriptor()
        ingestPayload = IngestPayload(ingestSourceDescriptor)
        ingestPayload.payload_inline = True

        task = AcceleratorWorkflowTask(xcom_props_resolver)
        task.report_individual(ingestPayload, runid, file_key, my_vals)

        self.assertTrue(len(ingestPayload.payload) == 1)
        self.assertTrue(len(ingestPayload.payload_path) == 0)

    def test_serialize_file(self):
        temp_dirs_path = "test_resources/temp_dirs"
        runid = "test_serialize_file"
        file_key = "mykey"
        path = os.path.join(temp_dirs_path, runid)

        if os.path.exists(path):
            shutil.rmtree(path)

        my_vals = {"mykey": "myvalue"}
        xcom_props_resolver = DirectXcomPropsResolver(temp_files_supported=True, temp_files_location=temp_dirs_path)

        ingestSourceDescriptor = IngestSourceDescriptor()
        ingestPayload = IngestPayload(ingestSourceDescriptor)
        ingestPayload.payload_inline = False

        task = AcceleratorWorkflowTask(xcom_props_resolver)
        task.report_individual(ingestPayload, runid, file_key, my_vals)

        self.assertTrue(len(ingestPayload.payload) == 0)
        self.assertTrue(len(ingestPayload.payload_path) == 1)


if __name__ == '__main__':
    unittest.main()
