import pathlib
import unittest

from accelerator_core.utils import resource_utils


class MyTestCase(unittest.TestCase):
    def test_determine_test_resource_path(self):
        actual = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        self.assertIsInstance(actual, pathlib.Path)


if __name__ == "__main__":
    unittest.main()
