import json
import unittest

from accelerator_core.utils.json_sanitizer import JSONSanitizer
from accelerator_core.utils.resource_utils import determine_test_resource_path


class TestSanitizeJson(unittest.TestCase):
    def test_sanitize(self):
        test_file = determine_test_resource_path(
            resource_name="sanitizeme.json", test_class="tests"
        )

        with open(test_file) as json_data:
            raw_data = json_data.read()
            sanitized = JSONSanitizer.sanitize_json_string(raw_data)
            self.assertIsNotNone(sanitized["description"])


if __name__ == "__main__":
    unittest.main()
