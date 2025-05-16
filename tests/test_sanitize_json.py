import json
import unittest

from accelerator_core.utils.json_sanitizer import JSONSanitizer


class TestSanitizeJson(unittest.TestCase):
    def test_sanitize(self):
        test_file = 'test_resources/sanitizeme.json'
        with open(test_file) as json_data:
            raw_data = json_data.read()
            sanitized = JSONSanitizer.sanitize_json_string(raw_data)
            self.assertIsNotNone(sanitized["description"])



if __name__ == '__main__':
    unittest.main()
