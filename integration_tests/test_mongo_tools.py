import unittest

from accelerator_core.utils import resource_utils, mongo_tools
from accelerator_core.utils.accelerator_config import AcceleratorConfig


class TestMongoToolsIntegration(unittest.TestCase):
    def test_drop_db(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "integration_tests"
        )
        config = AcceleratorConfig(test_path)
        client = mongo_tools.initialize_mongo_client(config)
        mongo_tools.drop_accel_database(client, config.properties["mongo.db.name"])

    def test_create_db(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "integration_tests"
        )
        config = AcceleratorConfig(test_path)
        client = mongo_tools.initialize_mongo_client(config)
        mongo_tools.create_accel_database(client, config.properties["mongo.db.name"])


if __name__ == "__main__":
    unittest.main()
