import unittest

from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.utils import resource_utils, mongo_tools
from accelerator_core.utils.accelerator_config import AcceleratorConfig, config_from_file


class TestMongoToolsIntegration(unittest.TestCase):

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

    def test_drop_db(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "integration_tests"
        )
        config = self.__class__._accelerator_config
        client = mongo_tools.initialize_mongo_client(config)
        mongo_tools.drop_accel_database(client, config.params["mongo.db.name"])

    def test_create_db(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "integration_tests"
        )
        config = self.__class__._accelerator_config
        client = mongo_tools.initialize_mongo_client(config)
        mongo_tools.create_accel_database(client, config.params["mongo.db.name"])

    @classmethod
    def tearDownClass(cls):
        cls._accel_db_context.mongo_client.close()


if __name__ == "__main__":
    unittest.main()
