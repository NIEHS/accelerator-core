import json
import unittest

import accelerator_core
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
        cls._mongo_client = mongo_tools.initialize_mongo_client(config)
        cls._accelerator_config = config

    @classmethod
    def tearDownClass(cls):
        cls._mongo_client.close()

    def test_validation(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            d = json.load(json_data)
            accession = AccessionMongo(self.__class__._accelerator_config)
            valid = accession.validate(d)
            self.assertTrue(valid)

    def test_ingest(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            d = json.load(json_data)
            accession = AccessionMongo(self.__class__._accelerator_config)
            id = accession.ingest(d)
            self.assertIsNotNone(id)


if __name__ == "__main__":
    unittest.main()
