import unittest

from accelerator_core.utils import resource_utils, mongo_tools
from accelerator_core.utils.accelerator_config import AcceleratorConfig


class TestMongoTools(unittest.TestCase):

    def setUp(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        matrix_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )
        self.config = AcceleratorConfig(
            config_path=test_path.as_posix(), type_matrix_path=matrix_path.as_posix()
        )

    def test_build_connectionString(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        config = self.config
        actual = mongo_tools.build_connection_string(config)
        self.assertIsNotNone(actual)


if __name__ == "__main__":
    unittest.main()
