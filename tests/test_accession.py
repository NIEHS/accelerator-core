import unittest
from unittest.mock import patch

from accelerator_core.services.accession import Accession
from accelerator_core.utils import resource_utils
from accelerator_core.utils.accelerator_config import config_from_file
from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_source_ingest import IngestSourceDescriptor


class TestAccessionValidation(unittest.TestCase):
    def setUp(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        self.config = config_from_file(test_path)
        self.config.find_type_matrix_info_for_type("accelerator").validate_json = False
        self.accession = Accession(
            self.config,
            DirectXcomPropsResolver(temp_files_supported=False, temp_files_location=""),
        )

    def test_skips_schema_validation_when_disabled(self):
        descriptor = IngestSourceDescriptor()
        descriptor.ingest_type = "accelerator"
        descriptor.schema_version = "1.0.3"

        with patch(
            "accelerator_core.services.accession.SchemaTools.validate_json_against_schema"
        ) as validate:
            result = self.accession.validate({"arbitrary": "document"}, descriptor)

        self.assertTrue(result.valid)
        validate.assert_not_called()


if __name__ == "__main__":
    unittest.main()
