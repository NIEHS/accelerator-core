import unittest
from accelerator_core.utils import resource_utils
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.type_matrix import TypeMatrix


class MyTestCase(unittest.TestCase):
    def test_get_accel_config_for_testing(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        matrix_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )
        actual = AcceleratorConfig(
            config_path=test_path.as_posix(), type_matrix_path=matrix_path.as_posix()
        )
        self.assertIsNotNone(actual.properties)

    def test_find_type_matrix_info_for_type(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        matrix_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )
        config = AcceleratorConfig(
            config_path=test_path.as_posix(), type_matrix_path=matrix_path.as_posix()
        )
        actual = config.find_type_matrix_info_for_type("accelerator")
        self.assertIsInstance(actual, TypeMatrix)


if __name__ == "__main__":
    unittest.main()
