import unittest
from accelerator_core.utils import resource_utils
from accelerator_core.utils.accelerator_config import AcceleratorConfig, config_from_file
from accelerator_core.utils.type_matrix import TypeMatrix


class MyTestCase(unittest.TestCase):
    def test_get_accel_config_for_testing(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        matrix_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )
        actual = config_from_file(test_path)
        self.assertIsNotNone(actual)

    def test_find_type_matrix_info_for_type(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        matrix_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )
        config = config_from_file(test_path)
        actual = config.find_type_matrix_info_for_type("accelerator")
        self.assertIsInstance(actual, TypeMatrix)


if __name__ == "__main__":
    unittest.main()
