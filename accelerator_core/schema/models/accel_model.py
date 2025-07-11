import json
import logging
import os

from jinja2 import Environment, FileSystemLoader

from accelerator_core.schema.models.base_model import (
    SubmissionInfoModel,
    TechnicalMetadataModel,
)
from accelerator_core.schema.templates.template_processor import AccelTemplateProcessor


class OtherType:
    """
    Value type that indicates whether a value is 'other', meaning it did not originate from
    the base schema.
    """

    def __init__(self, value):
        self.value = value
        self.other_type = False


class AccelProgramModel:
    """
    A program in accelerator
    """

    def __init__(self):
        self.name = ""
        self.code = ""
        self.preferred_label = ""


class AccelProjectModel:

    def __init__(self):
        self.code = ""
        self.name = ""
        self.short_name = ""
        self.project_sponsor = []
        self.project_url = ""


class ProjectSponsor:
    """
    Project sponsor and type
    """

    def __init__(self):
        self.sponsor = ""
        self.type = ""
        self.other_type = False


class AccelIntermediateResourceModel:
    """
    Represents an intermediate description of a resource
    """

    def __init__(self):
        self.name = ""
        self.version = ""
        self.short_name = ""
        self.resource_type = ""
        self.resource_url = ""
        self.description = ""
        self.domain = []
        self.keywords = []
        self.access_type = ""
        self.resource_reference = []
        self.resource_use_agreement = []
        self.publication = []
        self.is_static = False
        self.payment_required = False
        self.license_name = ""
        self.license_type = ""


class AccelDataResourceModel:
    """
    Data resource
    """

    def __init__(self):
        self.exposure_media = []
        self.measures = []
        self.measurement_method = ""
        self.time_extent_start = ""
        self.time_extent_end = ""
        self.time_available_comment = ""
        self.update_frequency = ""
        self.key_variables = []
        self.example_metrics = []
        self.data_formats = []
        self.data_location = []
        self.includes_citizen_collected = False
        self.has_api = False
        self.has_visualization_tool = False


class AccelPersonnelModel:
    """
    Modeling personnel connections to a resource
    """

    def __init__(self):
        self.name = ""
        self.affiliation = ""
        self.role = ""
        self.email = ""
        self.identifier = ""
        self.identifier_type = ""


class AccelResourceReferenceModel:
    """
    A resource reference
    """

    def __init__(self):
        self.resource_reference_text = ""
        self.resource_reference_link = ""


class AccelResourceUseAgreementModel:
    """
    Resource user agreement
    """

    def __init__(self):
        self.resource_use_agreement_text = ""
        self.resource_use_agreement_link = ""


class AccelPublicationModel:
    """
    Publication
    """

    def __init__(self):
        self.citation = ""
        self.citation_link = ""


class AccelDataLocationModel:
    """
    Data location
    """

    def __init__(self):
        self.data_location_text = ""
        self.data_location_link = ""


class AccelDataUsageModel:
    """
    Data usage characteristics
    """

    def __init__(self):
        self.intended_use = ""
        self.strengths = ""
        self.limitations = ""
        self.suggested_audience = ""


class AccelTemporalDataModel:
    """
    Temporal data
    """

    def __init__(self):
        self.temporal_resolution = []
        self.temporal_resolution_all_available = []
        self.temporal_resolution_comment = ""


class AccelPopulationDataModel:
    """
    Population data
    """

    def __init__(self):
        self.individual_level = False
        self.population_studies = []
        self.linkable_encounters = False
        self.biospecimens_from_humans = False
        self.biospecimens_type = []


class AccelGeospatialDataModel:
    """
    Geospatial Data
    """

    def __init__(self):
        self.spatial_resolution = []
        self.spatial_resolution_all_available = []
        self.spatial_resolution_comment = ""
        self.spatial_coverage = []
        self.spatial_bounding_box = []
        self.geometry_type = []
        self.geometry_source = []
        self.model_methods = []
        self.geographic_feature = []


class AccelComputationalWorkflow:
    """
    Tool/Computation related metadata
    """

    def __init__(self):
        self.tool_type = []
        self.is_open = False


def build_accel_from_model(
    version: str,
    submission: SubmissionInfoModel = SubmissionInfoModel(),
    technical: TechnicalMetadataModel = TechnicalMetadataModel,
    program: AccelPublicationModel = AccelPublicationModel(),
    project: AccelProjectModel = AccelProjectModel(),
    resource: AccelResourceReferenceModel = AccelResourceReferenceModel(),
    data_resource: AccelDataResourceModel = AccelDataResourceModel(),
    temporal: AccelTemporalDataModel = AccelTemporalDataModel(),
    population: AccelPopulationDataModel = AccelPopulationDataModel(),
    geospatial: AccelGeospatialDataModel = AccelGeospatialDataModel(),
) -> dict:
    """
    Build the json representation of the accelerator model, rendered via a template. Provide the components below,
    a component can be assigned 'None' except for submission and technical and default 'no values' will be generated
    :param version: string with x.x.x version
    :param submission: SubmissionInfoModel
    :param technical: TechnicalMetadataModel
    :param program: AccelProgramModel
    :param project: AccelProjectModel
    :param resource: AccelResourceReferenceModel
    :param data_resource: AccelDataResourceModel
    :param temporal: AccelTemporalDataModel
    :param population: AccelPopulationDataModel
    :param geospatial: AccelGeospatialDataModel
    :return: json document rendered as a dict
    """

    template_processor = AccelTemplateProcessor()
    template = template_processor.retrieve_template("accel", version)

    if submission is None:
        logging.error("No submission info provided")
        raise Exception("No submission info provided")

    if technical is None:
        logging.error("No technical info provided")
        raise Exception("No technical info provided")

    if program is None:
        logging.error("No program info provided")
        raise Exception("No program info provided")

    if project is None:
        logging.error("No project info provided")
        raise Exception("No project info provided")

    if resource is None:
        logging.error("No resource info provided")
        raise Exception("No resource info provided")

    if data_resource is None:
        data_resource = AccelDataResourceModel()

    if temporal is None:
        temporal = AccelTemporalDataModel()

    if population is None:
        population = AccelPopulationDataModel()

    if geospatial is None:
        geospatial = AccelGeospatialDataModel()

    rendered = template.render(
        version="1.0.0",
        submission=submission,
        technical_metadata=technical,
        program=program,
        project=project,
        resource=resource,
        data_resource=data_resource,
        temporal_data=temporal,
        geospatial_data=geospatial,
        population_data=population,
    )

    data = json.loads(rendered)

    return data
