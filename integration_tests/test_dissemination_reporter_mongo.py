import json
import unittest

from accelerator_core.schema.models.base_model import (
    DisseminationLinkReport,
    DisseminationEndpoint,
)
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.service_impls.mongo_accession import AccessionMongo
from accelerator_core.service_impls.mongo_dissemination import DisseminationMongo
from accelerator_core.service_impls.mongo_dissemination_reporter import (
    MongoDisseminationReporter,
)
from accelerator_core.utils import resource_utils
from accelerator_core.utils.accelerator_config import (
    config_from_file,
)
from accelerator_core.utils.resource_utils import (
    determine_test_resource_path,
)
from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationDescriptor
from accelerator_core.workflow.accel_source_ingest import (
    IngestSourceDescriptor,
    IngestPayload,
)


class TestDisseminationReporterMongo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "integration_tests"
        )
        matrix_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )

        config = config_from_file(test_path)

        accel_db_context = AccelDbContext(config)
        cls._accel_db_context = accel_db_context
        cls._accelerator_config = config

    @classmethod
    def tearDownClass(cls):
        cls._accel_db_context.mongo_client.close()

    def test_report_dissem(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_type = "accelerator"
        ingest_source_descriptor.schema_version = "1.0.2"
        ingest_source_descriptor.ingest_identifier = "test_report_dissem"
        ingest_source_descriptor.ingest_item_id = "test_report_dissem"
        ingest_source_descriptor.ingest_link = "mylink"
        ingest_source_descriptor.submitter_name = "mysubmittername"
        ingest_source_descriptor.submitter_email = "mysubmitteremail"
        ingest_source_descriptor.use_tempfiles = False

        ingest_result = IngestPayload(ingest_source_descriptor)

        json_path = determine_test_resource_path("example1.json", "integration_tests")
        with open(json_path) as json_data:
            d = json.load(json_data)
            ingest_result.payload.append(d)
            ingest_result.payload_inline = True

            xcom_props_resolver = DirectXcomPropsResolver(
                temp_files_supported=False, temp_files_location=""
            )

            accession = AccessionMongo(
                self.__class__._accelerator_config,
                self.__class__._accel_db_context,
                xcom_props_resolver,
            )

            id = accession.ingest(ingest_result, check_duplicates=False, temp_doc=False)
            self.assertIsNotNone(id)

            # now get the dissemination for this item

            dissemination_request = DisseminationDescriptor()
            dissemination_request.dissemination_type = "tests"
            dissemination_request.temp_collection = False
            dissemination_request.ingest_type = "accelerator"
            dissemination_request.schema_version = "1.0.2"
            dissemination_request.inline_results = True
            dissemination_request.dissemination_identifier = "test_dissemination"
            dissemination_request.dissemination_item_id = id

            dissemination = DisseminationMongo(
                self.__class__._accelerator_config,
                xcom_props_resolver,
                self.__class__._accel_db_context,
            )

            dissemination_payload = dissemination.disseminate_by_id(
                str(id), dissemination_request
            )

            self.assertIsNotNone(dissemination_payload)

            # now report a dissemination to dataverse

            link_report = DisseminationLinkReport()
            link_report.target_schema_type = "accelerator"
            link_report.target_schema_version = "1.0.2"
            link_report.temporary_data = False
            link_report.original_source_identifier = id

            endpoint = DisseminationEndpoint()
            endpoint.endpoint_type = "dataverse"
            endpoint.link = "https://dataverse.harvard.edu"
            endpoint.unique_identifier = "test_report_dissem"
            endpoint.date = "2022-01-01"

            link_report.dissemination_endpoint = endpoint

            dissemination_reporter = MongoDisseminationReporter(
                self.__class__._accelerator_config,
                xcom_props_resolver,
                self.__class__._accel_db_context,
            )

            dissemination_reporter.report_dissemination_result(link_report)

            actual = accession.find_by_id(id, ingest_source_descriptor.ingest_type)
            self.assertIsNotNone(actual)
            endpoints = actual["technical_metadata"]["dissemination_endpoints"]
            self.assertEqual(len(endpoints), 1)
            self.assertEqual(endpoints[0]["endpoint_type"], "dataverse")
            self.assertEqual(endpoints[0]["link"], "https://dataverse.harvard.edu")
            self.assertEqual(endpoints[0]["unique_identifier"], "test_report_dissem")
            self.assertEqual(endpoints[0]["date"], "2022-01-01")

            # now force an update to a new date and check

            link_report = DisseminationLinkReport()
            link_report.target_schema_type = "accelerator"
            link_report.target_schema_version = "1.0.2"
            link_report.temporary_data = False
            link_report.original_source_identifier = id

            endpoint = DisseminationEndpoint()
            endpoint.endpoint_type = "dataverse"
            endpoint.link = "https://dataverse.harvard.edu"
            endpoint.unique_identifier = "test_report_dissem"
            endpoint.date = "2022-01-02"
            link_report.dissemination_endpoint = endpoint

            dissemination_reporter.report_dissemination_result(link_report)

            actual = accession.find_by_id(id, ingest_source_descriptor.ingest_type)
            self.assertIsNotNone(actual)
            endpoints = actual["technical_metadata"]["dissemination_endpoints"]
            self.assertEqual(len(endpoints), 1)
            self.assertEqual(endpoints[0]["endpoint_type"], "dataverse")
            self.assertEqual(endpoints[0]["link"], "https://dataverse.harvard.edu")
            self.assertEqual(endpoints[0]["unique_identifier"], "test_report_dissem")
            self.assertEqual(endpoints[0]["date"], "2022-01-02")
