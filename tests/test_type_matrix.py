import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from accelerator_core.utils import resource_utils
from accelerator_core.utils.type_matrix import parse_type_matrix


class TestTypeMatrix(unittest.TestCase):
    def test_parse(self):
        test_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )
        actual = parse_type_matrix(test_path)
        self.assertIsNotNone(actual)
        self.assertEqual("accelerator", actual[0].type)
        self.assertTrue(actual[0].validate_json)

    def test_validate_json_must_be_boolean(self):
        with TemporaryDirectory() as temp_dir:
            matrix_path = Path(temp_dir) / "type_matrix.yaml"
            matrix_path.write_text(
                "types:\n"
                "- name: accelerator\n"
                "  schema: accel-schema\n"
                "  validate_json: \"yes\"\n"
                "  collection: accelerator\n"
                "  temp_collection: accelerator_temp\n"
                "  default_version: 1.0.2\n"
            )

            with self.assertRaises(ValueError):
                parse_type_matrix(matrix_path)


if __name__ == "__main__":
    unittest.main()
