import unittest

from accelerator_core.workflow.accel_data_models import (
    DisseminationDescriptor,
    DisseminationPayload,
)

from accelerator_core.workflow.accel_source_ingest import (
    IngestSourceDescriptor,
    IngestPayload,
)


class TestDictSerialization(unittest.TestCase):
    def test_ingest_source_description(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_format = "format"
        ingest_source_descriptor.ingest_link = "link"
        ingest_source_descriptor.ingest_type = "type"
        ingest_source_descriptor.ingest_identifier = "identifier"
        ingest_source_descriptor.source_metadata_reference_link = (
            "source_metadata_reference_link"
        )
        ingest_source_descriptor.batch = False
        ingest_source_descriptor.schema_version = "schema_version"
        ingest_source_descriptor.submitter_email = "submitter_email"
        ingest_source_descriptor.submitter_name = "submitter_name"
        ingest_source_descriptor.submit_date = "submit_date"

        actual = ingest_source_descriptor.to_dict()
        self.assertIsNotNone(actual)

        actual_from_dict = IngestSourceDescriptor.from_dict(actual)
        self.assertEqual(actual_from_dict.ingest_format, "format")
        self.assertEqual(actual_from_dict.ingest_link, "link")
        self.assertEqual(actual_from_dict.ingest_type, "type")
        self.assertEqual(actual_from_dict.ingest_identifier, "identifier")

        self.assertEqual(actual_from_dict.schema_version, "schema_version")
        self.assertEqual(actual_from_dict.submitter_email, "submitter_email")
        self.assertEqual(actual_from_dict.submitter_name, "submitter_name")
        self.assertEqual(actual_from_dict.submit_date, "submit_date")

    def test_ingest_payload(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_format = "format"
        ingest_source_descriptor.ingest_link = "link"
        ingest_source_descriptor.ingest_type = "type"
        ingest_source_descriptor.ingest_identifier = "identifier"
        ingest_source_descriptor.source_metadata_reference_link = (
            "source_metadata_reference_link"
        )
        ingest_source_descriptor.batch = False
        ingest_source_descriptor.schema_version = "schema_version"
        ingest_source_descriptor.submitter_email = "submitter_email"
        ingest_source_descriptor.submitter_name = "submitter_name"
        ingest_source_descriptor.submit_date = "submit_date"

        ingest_payload = IngestPayload(ingest_source_descriptor)
        ingest_payload.ingest_source_descriptor = ingest_source_descriptor
        ingest_payload.source_document_detail = "source_document_detail"
        ingest_payload.ingest_successful = "ingest_successful"
        ingest_payload.payload_inline = True
        ingest_payload.payload = []
        ingest_payload.payload_path = []

        actual = ingest_payload.to_dict()
        self.assertIsNotNone(actual)

        actual_from_dict = IngestPayload.from_dict(actual)
        self.assertEqual(
            ingest_payload.ingest_successful, actual_from_dict.ingest_successful
        )
        self.assertEqual(ingest_payload.payload_inline, actual_from_dict.payload_inline)
        self.assertEqual(ingest_payload.payload_path, actual_from_dict.payload_path)

    def test_dissemination_descriptor(self):
        dissemination_descriptor = DisseminationDescriptor()
        dissemination_descriptor.dissemination_identifier = "dissemination_identifier"
        dissemination_descriptor.ingest_type = "type"
        dissemination_descriptor.schema_version = "schema_version"
        dissemination_descriptor.submitter_email = "submitter_email"
        dissemination_descriptor.submitter_name = "submitter_name"
        dissemination_descriptor.submit_date = "submit_date"

        dictversion = dissemination_descriptor.to_dict()
        actual = DisseminationDescriptor.from_dict(dictversion)
        self.assertIsNotNone(actual)
        self.assertEqual(dissemination_descriptor.ingest_type, actual.ingest_type)
        self.assertEqual(
            dissemination_descriptor.dissemination_identifier,
            actual.dissemination_identifier,
        )
        self.assertEqual(dissemination_descriptor.schema_version, actual.schema_version)
        self.assertEqual(
            dissemination_descriptor.submitter_email, actual.submitter_email
        )
        self.assertEqual(dissemination_descriptor.submitter_name, actual.submitter_name)
        self.assertEqual(dissemination_descriptor.submit_date, actual.submit_date)

    def test_dissemination_payload(self):
        dissemination_descriptor = DisseminationDescriptor()
        dissemination_descriptor.dissemination_identifier = "dissemination_identifier"
        dissemination_descriptor.ingest_type = "type"
        dissemination_descriptor.schema_version = "schema_version"
        dissemination_descriptor.submitter_email = "submitter_email"
        dissemination_descriptor.submitter_name = "submitter_name"
        dissemination_descriptor.submit_date = "submit_date"

        dissemination_payload = DisseminationPayload(dissemination_descriptor)
        dictversion = dissemination_payload.to_dict()
        actual = DisseminationPayload.from_dict(dictversion)
        self.assertIsNotNone(actual)


if __name__ == "__main__":
    unittest.main()
