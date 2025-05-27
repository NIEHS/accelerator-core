import json
import unittest
from shlex import shlex

import accelerator_core
from accelerator_core.schema.models.accel_model import (
    AccelProgramModel,
    AccelProjectModel,
    AccelIntermediateResourceModel,
    AccelResourceReferenceModel,
    AccelResourceUseAgreementModel,
    AccelPublicationModel,
    AccelDataResourceModel,
    AccelDataLocationModel,
    AccelGeospatialDataModel,
    AccelTemporalDataModel,
    AccelPopulationDataModel,
)
from accelerator_core.schema.models.base_model import (
    SubmissionInfoModel,
    TechnicalMetadataModel,
)
from accelerator_core.utils import resource_utils
from accelerator_core.utils.accelerator_config import AcceleratorConfig, config_from_file
from accelerator_core.utils.schema_tools import SchemaTools
from accelerator_core.schema.models.accel_model import build_accel_from_model


class TestAccelModel(unittest.TestCase):

    def setUp(self):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )
        matrix_path = resource_utils.determine_test_resource_path(
            "test_type_matrix.yaml", "tests"
        )

        self.config = config_from_file(test_path)


    def test_build_and_validate_accel(self):

        submission = SubmissionInfoModel()
        submission.submitter_comment = "comment"
        submission.submitter_email = "submitter@email.com"
        submission.submitter_name = "submitter_name"

        program = AccelProgramModel()
        program.code = "code"
        program.name = "name"
        program.preferred_label = "preferred_label"

        project = AccelProjectModel()
        project.code = "code"
        project.name = "name"
        project.project_sponsor = ["sponsor1"]
        project.project_sponsor_other = ["sponsor2"]
        project.project_sponsor_type = ["sponsor_type1"]
        project.project_sponsor_type_other = ["sponsor_type2"]
        project.project_ur = "http://project.url.com"

        resource = AccelIntermediateResourceModel()
        resource.name = "rescname"
        resource.version = "1.0.0"
        resource.resource_type = "boo"
        resource.resource_url = "http://resc.url.com"
        resource.description = "description"
        resource.keywords = ["keyword1", "keyword2"]
        reference = AccelResourceReferenceModel
        reference.resource_reference_text = "text"
        reference.resource_reference_link = "http://reference.url.com"
        resource.resource_reference = [reference]
        use_agreement = AccelResourceUseAgreementModel
        use_agreement.resource_user_agreement_text = "text"
        use_agreement.resource_user_agreement_link = "http://agreement.url.com"
        resource.resource_use_agreement = [use_agreement]
        publication = AccelPublicationModel
        publication.citation = "cite"
        publication.citation_text = "http://citation.link.com"
        resource.publication = [publication]
        resource.is_static = True

        data_resource = AccelDataResourceModel()
        data_resource.exposure_media = ["media1"]
        data_resource.measures = ["measure1"]
        data_resource.measures_other = ["measure2"]
        data_resource.time_extent_start = "2014"
        data_resource.time_extent_end = "2015"
        data_resource.data_formats = [".gif"]
        location = AccelDataLocationModel
        location.data_location_text = "text"
        location.data_location_link = "http://location.link.com"
        data_resource.data_location = [location]

        geospatial = AccelGeospatialDataModel()
        geospatial.spatial_resolution = ["1 km"]
        geospatial.coverage = ["continental US"]
        model_methods = ["method1", "method2"]

        temporal = AccelTemporalDataModel()
        temporal.temporal_resolution = ["res1"]
        temporal.temporal_resolution_comment = "comment"

        technical = TechnicalMetadataModel()
        technical.original_source = "a test"

        population_data = AccelPopulationDataModel()
        population_data.population_studies = ["study1"]

        rendered = build_accel_from_model(
            version="1.0.0",
            submission=submission,
            technical=technical,
            program=program,
            project=project,
            resource=resource,
            data_resource=data_resource,
            temporal=temporal,
            geospatial=geospatial,
            population=population_data,
        )

        schema_tools = SchemaTools(self.config)
        result = schema_tools.validate_json_against_schema(
            rendered, "accelerator", "1.0.0"
        )
        self.assertTrue(result.valid)
