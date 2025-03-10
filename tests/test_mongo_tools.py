import unittest

from accelerator_core.utils import resource_utils, mongo_tools
from accelerator_core.utils.accelerator_config import AcceleratorConfig


class TestMongoTools(unittest.TestCase):
    def test_build_connectionString(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        config = AcceleratorConfig(test_path)
        actual = mongo_tools.build_connection_string(config)
        self.assertIsNotNone(actual)


if __name__ == "__main__":
    unittest.main()
