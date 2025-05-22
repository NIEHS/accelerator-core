import json
import unittest

import accelerator_core
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.service_impls.mongo_accession import AccessionMongo
from accelerator_core.service_impls.mongo_dissemination import DisseminationMongo
from accelerator_core.services.dissemination import DisseminationDescriptor
from accelerator_core.utils import resource_utils, mongo_tools
from accelerator_core.utils.accel_exceptions import AccelDocumentNotFoundException
from accelerator_core.utils.accelerator_config import AcceleratorConfig, config_from_file
from accelerator_core.utils.resource_utils import (
    determine_resource_path,
    determine_test_resource_path,
)
from accelerator_core.workflow.accel_source_ingest import (
    IngestSourceDescriptor,
    IngestPayload,
)


class TestDisseminationMongo(unittest.TestCase):

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

    def test_dissemination(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_type = "accelerator"
        ingest_source_descriptor.schema_version = "1.0.0"

        ingest_result = IngestPayload(ingest_source_descriptor)

        json_path = determine_test_resource_path("example1.json", "integration_tests")
        with open(json_path) as json_data:
            d = json.load(json_data)
            ingest_result.payload.append(d)
            ingest_result.payload_inline = True

            accession = AccessionMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )

            id = accession.ingest(ingest_result, check_duplicates=False, temp_doc=False)
            self.assertIsNotNone(id)

            # now get the dissemination for this item

            dissemination_request = DisseminationDescriptor()
            dissemination_request.dissemination_type = "test"
            dissemination_request.temp_collection = "false"
            dissemination_request.ingest_type = "accelerator"
            dissemination_request.schema_version = "1.0.0"
            dissemination_request.inline_results = True

            dissemination = DisseminationMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )
            dissemination_payload = dissemination.disseminate_by_id(
                id, dissemination_request
            )

            self.assertIsNotNone(dissemination_payload)

    def test_dissemination_not_found(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        id = "95E43738404BEECDF66573B4"
        dissemination_request = DisseminationDescriptor()
        dissemination_request.dissemination_type = "test"
        dissemination_request.temp_collection = "false"
        dissemination_request.ingest_type = "accelerator"
        dissemination_request.schema_version = "1.0.0"
        dissemination_request.inline_results = True

        dissemination = DisseminationMongo(
            self.__class__._accelerator_config, self.__class__._accel_db_context
        )
        with self.assertRaises(AccelDocumentNotFoundException) as context:
            dissemination.disseminate_by_id(id, dissemination_request)
