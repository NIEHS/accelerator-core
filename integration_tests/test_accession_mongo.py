import json
import unittest

import accelerator_core
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.service_impls.mongo_accession import AccessionMongo
from accelerator_core.utils import resource_utils, mongo_tools
from accelerator_core.utils.accelerator_config import AcceleratorConfig, config_from_file
from accelerator_core.utils.resource_utils import determine_resource_path
from accelerator_core.workflow.accel_source_ingest import (
    IngestSourceDescriptor,
    IngestPayload,
)


class TestAccessionMongo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "integration_tests"
        )
        matrix_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )

        config = config_from_file(test_path)

        accel_db_context = AccelDbContext(config)
        cls._accel_db_context = accel_db_context
        cls._accelerator_config = config

    @classmethod
    def tearDownClass(cls):
        cls._accel_db_context.mongo_client.close()

    def test_validation(self):

        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_type = "accelerator"
        ingest_source_descriptor.schema_version = "1.0.0"

        json_path = determine_resource_path(accelerator_core.schema, "accel.json")

        with open(json_path) as json_data:
            d = json.load(json_data)
            accession = AccessionMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )
            result = accession.validate(d, ingest_source_descriptor)
            self.assertTrue(result.valid)

    def test_ingest(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_type = "accelerator"
        ingest_source_descriptor.schema_version = "1.0.0"

        ingest_result = IngestPayload(ingest_source_descriptor)

        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            d = json.load(json_data)
            ingest_result.payload.append(d)
            ingest_result.payload_inline = True

            accession = AccessionMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )

            id = accession.ingest(ingest_result, check_duplicates=False, temp_doc=False)
            self.assertIsNotNone(id)

            # now look up the doc in the expected collection

            actual = accession.find_by_id(id, ingest_source_descriptor.ingest_type)
            self.assertIsNotNone(actual)

    def test_find_by_id(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            ingest_source_descriptor = IngestSourceDescriptor()
            ingest_source_descriptor.ingest_type = "accelerator"
            ingest_source_descriptor.schema_version = "1.0.0"

            ingest_result = IngestPayload(ingest_source_descriptor)

            d = json.load(json_data)
            ingest_result.payload.append(d)
            ingest_result.payload_inline = True

            accession = AccessionMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )

            id = accession.ingest(ingest_result, check_duplicates=False, temp_doc=False)
            actual = accession.find_by_id(id, ingest_source_descriptor.ingest_type)
            self.assertIsNotNone(actual)
            self.assertIsInstance(actual, dict)

    def test_decommission(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            ingest_source_descriptor = IngestSourceDescriptor()
            ingest_source_descriptor.ingest_type = "accelerator"
            ingest_source_descriptor.schema_version = "1.0.0"

            ingest_result = IngestPayload(ingest_source_descriptor)

            d = json.load(json_data)
            ingest_result.payload.append(d)
            ingest_result.payload_inline = True

            accession = AccessionMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )

            id = accession.ingest(ingest_result, check_duplicates=False, temp_doc=False)
            accession.decommission(id, ingest_source_descriptor.ingest_type)
            actual = accession.find_by_id(id, ingest_source_descriptor.ingest_type)
            self.assertIsNone(actual)

    def test_delete_temp_document(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            ingest_source_descriptor = IngestSourceDescriptor()
            ingest_source_descriptor.ingest_type = "accelerator"
            ingest_source_descriptor.schema_version = "1.0.0"

            ingest_result = IngestPayload(ingest_source_descriptor)

            d = json.load(json_data)
            ingest_result.payload.append(d)
            ingest_result.payload_inline = True

            accession = AccessionMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )

            id = accession.ingest(ingest_result, check_duplicates=False, temp_doc=True)
            accession.delete_temp_document(id, ingest_source_descriptor.ingest_type)
            actual = accession.find_by_id(id, ingest_source_descriptor.ingest_type)
            self.assertIsNone(actual)


if __name__ == "__main__":
    unittest.main()
