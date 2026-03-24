import json
import unittest

from accelerator_core.utils.xcom_utils import (
    XcomPropsResolver,
    DirectXcomPropsResolver,
    XcomUtils,
)

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

    def test_write_temp_file(self):
        xcom_dir = determine_test_resource_path("test_resources/temp_dirs")
        xcom_props = DirectXcomPropsResolver(
            temp_files_supported=True,
            temp_files_location=xcom_dir.absolute().as_posix(),
        )
        xcom_utils = XcomUtils(xcom_props)

        my_bytes = b"mybytes"
        actual = xcom_utils.store_temp_data(my_bytes)
        self.assertIsNotNone(actual)


if __name__ == "__main__":
    unittest.main()
