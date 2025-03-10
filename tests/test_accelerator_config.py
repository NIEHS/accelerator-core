import unittest
from accelerator_core.utils import resource_utils
from accelerator_core.utils.accelerator_config import AcceleratorConfig


class MyTestCase(unittest.TestCase):
    def test_get_accel_config_for_testing(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        actual = AcceleratorConfig(test_path)
        self.assertIsNotNone(actual.properties)


if __name__ == "__main__":
    unittest.main()
