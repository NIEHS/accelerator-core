import json
import unittest

import accelerator_core
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.service_impls.mongo_accession import AccessionMongo
from accelerator_core.service_impls.mongo_dissemination import DisseminationMongo
from accelerator_core.utils import resource_utils
from accelerator_core.utils.accel_database_utils import AccelDatabaseUtils
from accelerator_core.utils.accel_exceptions import AccelDocumentNotFoundException
from accelerator_core.utils.accelerator_config import (
    config_from_file,
)
from accelerator_core.utils.resource_utils import (
    determine_resource_path,
    determine_test_resource_path,
)
from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationDescriptor
from accelerator_core.workflow.accel_source_ingest import (
    IngestSourceDescriptor,
    IngestPayload,
)
from utils.data_utils import generate_guid


class TestDisseminationMongo(unittest.TestCase):

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

    def setUp(self):
        accel_database_utils = AccelDatabaseUtils(
            self.__class__._accelerator_config, self.__class__._accel_db_context
        )
        accel_database_utils.clear_collection("accelerator", temp_doc=False)

    def test_dissemination(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_type = "accelerator"
        ingest_source_descriptor.schema_version = "1.0.3"
        ingest_source_descriptor.ingest_identifier = "myrunid"
        ingest_source_descriptor.ingest_item_id = "myitemid"
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
            dissemination_request.schema_version = "1.0.3"
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

    def test_find_doc_by_original_source_identifier(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_type = "accelerator"
        ingest_source_descriptor.schema_version = "1.0.3"
        ingest_source_descriptor.ingest_identifier = "myrunid"
        ingest_source_descriptor.ingest_item_id = "test_find_one_by_filter"
        ingest_source_descriptor.ingest_link = "mylink"
        ingest_source_descriptor.submitter_name = "mysubmittername"
        ingest_source_descriptor.submitter_email = "mysubmitteremail"
        ingest_result = IngestPayload(ingest_source_descriptor)

        json_path = determine_resource_path(
            accelerator_core.schema, "accel-v1.0.3.json"
        )
        with open(json_path) as json_data:
            d = json.load(json_data)

            d["technical_metadata"][
                "original_source_identifier"
            ] = ingest_source_descriptor.ingest_item_id
            d["technical_metadata"][
                "original_source_link"
            ] = ingest_source_descriptor.ingest_link

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

            dissemination = DisseminationMongo(
                self.__class__._accelerator_config,
                xcom_props_resolver,
                self.__class__._accel_db_context,
            )

            actual = dissemination.accel_database_utils.find_doc_by_original_source_identifier(
                ingest_source_descriptor.ingest_type,
                ingest_source_descriptor.ingest_link,
                ingest_source_descriptor.ingest_item_id,
            )

            self.assertIsNotNone(actual)

    def test_disseminate_by_original_source_and_id(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_type = "accelerator"
        ingest_source_descriptor.schema_version = "1.0.3"
        ingest_source_descriptor.ingest_identifier = "myrunid"
        ingest_source_descriptor.ingest_item_id = (
            "test_disseminate_by_original_source_and_id"
        )
        ingest_source_descriptor.ingest_link = "ingest_source"
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
            dissemination_request.dissemination_type = "dataverse"
            dissemination_request.temp_collection = False
            dissemination_request.ingest_type = "accelerator"
            dissemination_request.schema_version = "1.0.3"
            dissemination_request.inline_results = True
            dissemination_request.dissemination_identifier = "test_dissemination"
            dissemination_request.dissemination_item_id = id

            dissemination = DisseminationMongo(
                self.__class__._accelerator_config,
                xcom_props_resolver,
                self.__class__._accel_db_context,
            )

            dissemination_payload = dissemination.disseminate_by_original_source_and_id(
                ingest_source_descriptor.ingest_link,
                ingest_source_descriptor.ingest_item_id,
                dissemination_request,
            )

            self.assertIsNotNone(dissemination_payload)

    def test_disseminate_by_filter(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        ingest_source_descriptor.ingest_type = "accelerator"
        ingest_source_descriptor.schema_version = "1.0.3"
        ingest_source_descriptor.ingest_identifier = "myrunid"

        ingest_source_descriptor.ingest_link = "cedar"
        ingest_source_descriptor.submitter_name = "mysubmittername"
        ingest_source_descriptor.submitter_email = "mysubmitteremail"
        ingest_source_descriptor.use_tempfiles = False

        ingest_result = IngestPayload(ingest_source_descriptor)

        json_path = determine_test_resource_path(
            "test_corpus.json", "integration_tests"
        )

        coll = self._accel_db_context.build_collection_reference(
            self._accel_db_context.db, "accelerator"
        )

        with open(json_path) as json_data:
            d = json.load(json_data)

            for doc in d:

                del doc["_id"]
                coll.insert_one(doc)

        dissemination_payloads = []

        filter = {
            "technical_metadata.original_source_link": "cedar",
            "technical_metadata.dissemination_endpoints": {
                "$not": {"$elemMatch": {"endpoint_type": "cafe"}}
            },
        }

        dissemination_request = DisseminationDescriptor()
        dissemination_request.dissemination_type = "cafe"
        dissemination_request.temp_collection = False
        dissemination_request.ingest_type = "accelerator"
        guid = generate_guid()
        dissemination_request.run_id = guid
        dissemination_request.dissemination_identifier = guid
        dissemination_request.schema_version = "1.0.3"
        dissemination_request.dissemination_filter = filter

        xcom_props_resolver = DirectXcomPropsResolver(
            temp_files_supported=False, temp_files_location=""
        )

        dissemination = DisseminationMongo(
            self.__class__._accelerator_config,
            xcom_props_resolver,
            self.__class__._accel_db_context,
        )

        dissemination_payloads = dissemination.disseminate_by_filter(
            dissemination_request
        )

        self.assertIsNotNone(dissemination_payloads)

    def test_dissemination_not_found(self):
        ingest_source_descriptor = IngestSourceDescriptor()
        id = "95E43738404BEECDF66573B4"
        dissemination_request = DisseminationDescriptor()
        dissemination_request.dissemination_type = "tests"
        dissemination_request.temp_collection = "false"
        dissemination_request.ingest_type = "accelerator"
        dissemination_request.schema_version = "1.0.3"
        dissemination_request.inline_results = True

        xcom_props_resolver = DirectXcomPropsResolver(
            temp_files_supported=False, temp_files_location=""
        )

        dissemination = DisseminationMongo(
            self.__class__._accelerator_config,
            xcom_props_resolver,
            self.__class__._accel_db_context,
        )

        with self.assertRaises(AccelDocumentNotFoundException) as context:
            dissemination.disseminate_by_id(id, dissemination_request)
