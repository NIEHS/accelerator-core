import unittest

from bson import ObjectId

from accelerator_core.utils import resource_utils, mongo_tools
from accelerator_core.utils.accel_database_utils import AccelDatabaseUtils
from accelerator_core.utils.accelerator_config import (
    config_from_file,
)


class TestMongoTools(unittest.TestCase):

    def setUp(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        matrix_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )
        self.config = config_from_file(test_path.as_posix())

    def test_build_connectionString(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        config = self.config
        actual = mongo_tools.build_connection_string(config)
        self.assertIsNotNone(actual)

    def test_mongo_direct(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        config = self.config
        actual = mongo_tools.is_mongo_direct(config)
        self.assertTrue(actual)

    def test_extract_id_from_native_object_id(self):
        document_id = ObjectId()
        self.assertEqual(
            str(document_id),
            AccelDatabaseUtils.extract_id_from_doc({"_id": document_id}),
        )


if __name__ == "__main__":
    unittest.main()
