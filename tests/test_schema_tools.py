import json
import unittest
from shlex import shlex

import accelerator_core
from accelerator_core.utils import resource_utils
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.resource_utils import determine_resource_path
from accelerator_core.utils.schema_tools import SchemaTools


class TestSchemaTools(unittest.TestCase):

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

    def test_read_current_schema(self):

        schema_tools = SchemaTools(self.config)
        schema_json = schema_tools.read_current_schema("accelerator")

        self.assertIsNotNone(schema_json, "did not schema ")
        self.assertIsInstance(schema_json, dict)

    def test_validate_schema(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            d = json.load(json_data)

            schema_tools = SchemaTools(self.config)
            actual = schema_tools.validate_json_against_schema(d, "accelerator")
            self.assertTrue(actual, "Did not validate json against schema")


if __name__ == "__main__":
    unittest.main()
