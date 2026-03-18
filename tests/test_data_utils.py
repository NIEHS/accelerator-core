import json
import unittest

from accelerator_core.utils.data_utils import checksum_data
from accelerator_core.utils.resource_utils import determine_test_resource_path


class TestDataUtils(unittest.TestCase):
    def test_checksum(self):
        test_file = determine_test_resource_path(
            resource_name="mongo_item.json", test_class="tests"
        )

        with open(test_file) as json_data:
            payload = json.load(json_data)
            checksum = checksum_data(payload)
            self.assertIsNotNone(checksum)


if __name__ == "__main__":
    unittest.main()
