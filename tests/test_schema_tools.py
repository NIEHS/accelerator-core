import json
import unittest

import accelerator_core
from accelerator_core.utils.resource_utils import determine_resource_path
from accelerator_core.utils.schema_tools import (
    read_current_schema,
    validate_json_against_schema,
)


class TestSchemaTools(unittest.TestCase):
    def test_read_current_schema(self):
        schema_json = read_current_schema()
        self.assertIsNotNone(schema_json, "did not schema ")
        self.assertIsInstance(schema_json, dict)

    def test_validate_schema(self):
        json_path = determine_resource_path(accelerator_core.schema, "accel.json")
        with open(json_path) as json_data:
            d = json.load(json_data)

            actual = validate_json_against_schema(d)
            self.assertTrue(actual, "Did not validate json against schema")


if __name__ == "__main__":
    unittest.main()
