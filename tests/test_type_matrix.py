import unittest

from accelerator_core.utils import resource_utils
from accelerator_core.utils.type_matrix import parse_type_matrix, TypeMatrix


class TestTypeMatrix(unittest.TestCase):
    def test_parse(self):
        test_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )
        actual = parse_type_matrix(test_path)
        self.assertIsNotNone(actual)
        self.assertEqual("pcor", actual[0].type)


if __name__ == "__main__":
    unittest.main()
