import pathlib
import unittest

import accelerator_core
from accelerator_core.utils import resource_utils


class TestResourceUtils(unittest.TestCase):

    def test_determine_test_resource_path(self):
        actual = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        self.assertIsInstance(actual, pathlib.Path)

    def test_determine_resource_path(self):
        actual = resource_utils.determine_resource_path("accelerator_core.schema", "type_matrix.yaml")
        self.assertIsNotNone(actual)


if __name__ == "__main__":
    unittest.main()
