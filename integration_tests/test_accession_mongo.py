import json
import unittest

import accelerator_core
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.service_impls.mongo_accession import AccessionMongo
from accelerator_core.utils import resource_utils, mongo_tools
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.resource_utils import determine_resource_path


class TestAccessionMongo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "integration_tests"
        )
        config = AcceleratorConfig(test_path)
        accel_db_context = AccelDbContext(config)
        cls._accel_db_context = accel_db_context
        cls._accelerator_config = config

    @classmethod
    def tearDownClass(cls):
        cls._accel_db_context.mongo_client.close()

    def test_validation(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            d = json.load(json_data)
            accession = AccessionMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )
            valid = accession.validate(d)
            self.assertTrue(valid)

    def test_ingest(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            d = json.load(json_data)
            accession = AccessionMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )
            id = accession.ingest(d)
            self.assertIsNotNone(id)

    def test_find_by_id(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            d = json.load(json_data)
            accession = AccessionMongo(
                self.__class__._accelerator_config, self.__class__._accel_db_context
            )
            id = accession.ingest(d)
            actual = accession.find_by_id(id)
            self.assertIsNotNone(actual)
            self.assertIsInstance(actual, dict)


if __name__ == "__main__":
    unittest.main()
