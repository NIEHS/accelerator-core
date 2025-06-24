import os
import shutil
import unittest

from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_source_ingest import (
    IngestPayload,
    IngestSourceDescriptor,
)
from accelerator_core.workflow.accel_workflow_task import AcceleratorWorkflowTask


class TestAcceleratorWorkflowTask(unittest.TestCase):
    def test_serialize_inline(self):
        temp_dirs_path = "test_resources/temp_dirs"
        runid = "test_serialize_inline"
        file_key = "mykey"
        path = os.path.join(temp_dirs_path, runid)

        if os.path.exists(path):
            shutil.rmtree(path)

        my_vals = {"mykey": "myvalue"}
        xcom_props_resolver = DirectXcomPropsResolver(
            temp_files_supported=True, temp_files_location=temp_dirs_path
        )

        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_identifier = "tests"
        inline_ingest_payload = IngestPayload(ingest_source_descriptor)
        inline_ingest_payload.payload_inline = True

        task = AcceleratorWorkflowTask(xcom_props_resolver)
        task.report_individual(inline_ingest_payload, file_key, my_vals)

        self.assertTrue(len(inline_ingest_payload.payload) == 1)
        self.assertTrue(len(inline_ingest_payload.payload_path) == 0)

    def test_serialize_file(self):
        temp_dirs_path = "test_resources/temp_dirs"
        runid = "test_serialize_file"
        file_key = "mykey"
        path = os.path.join(temp_dirs_path, runid)

        if os.path.exists(path):
            shutil.rmtree(path)

        my_vals = {"mykey": "myvalue"}
        xcom_props_resolver = DirectXcomPropsResolver(
            temp_files_supported=True, temp_files_location=temp_dirs_path
        )

        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_identifier = "tests"
        ingest_source_descriptor.use_tempfiles = True
        serialized_ingest_payload = IngestPayload(ingest_source_descriptor)

        task = AcceleratorWorkflowTask(xcom_props_resolver)
        task.report_individual(serialized_ingest_payload, file_key, my_vals)

        self.assertTrue(len(serialized_ingest_payload.payload) == 0)
        self.assertTrue(len(serialized_ingest_payload.payload_path) == 1)

    def test_payload_resolve(self):
        temp_dirs_path = "test_resources/temp_dirs"
        runid = "test_payload_resolve"
        file_key = "mykey"
        path = os.path.join(temp_dirs_path, runid)

        if os.path.exists(path):
            shutil.rmtree(path)

        my_vals = {"mykey": "myvalue"}
        xcom_props_resolver = DirectXcomPropsResolver(
            temp_files_supported=True, temp_files_location=temp_dirs_path
        )

        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_identifier = "tests"
        ingest_source_descriptor.use_tempfiles = True
        ingest_payload = IngestPayload(ingest_source_descriptor)
        ingest_payload.payload_inline = False

        task = AcceleratorWorkflowTask(xcom_props_resolver)
        task.report_individual(ingest_payload, file_key, my_vals)

        actual = task.payload_resolve(ingest_payload, 0)
        self.assertTrue(actual == my_vals)
        self.assertFalse(ingest_payload.payload_inline)


if __name__ == "__main__":
    unittest.main()
