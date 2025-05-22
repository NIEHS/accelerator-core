import importlib.resources

from cfgv import ValidationError

from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.logger import setup_logger
import accelerator_core.schema
from accelerator_core.utils.resource_utils import determine_resource_path
import json
import jsonschema

logger = setup_logger("accelerator")

CURRENT_JSON_SCHEMA_VERSION = "2020-12"


class SchemaValidationResult:
    """
    Result of a schema validation operation
    """

    def __init__(
        self,
        valid: bool,
        schema_type: str,
        schema_version: str,
        json_doc: dict,
        schema_doc: dict,
        error: ValidationError = None,
    ):
        """
        Response from a schema validation operation
        :param valid: True if the schema is valid
        :param schema_type: schema type in accel
        :param schema_version: version of accel schema to validate against, as a version string: 1.0.0,
        :param json_doc: dict with source json
        :param schema_doc: dict with schema doc
        :param error: ValidationError or None if valid
        """
        self.valid = valid
        self.schema_type = schema_type
        self.schema_version = schema_version
        self.json_doc = json_doc
        self.schema_doc = schema_doc
        self.error = error
        if error:
            self.error_message = error.message
        else:
            self.error_message = ""


class SchemaTools:
    """
    Represents validation schema and validation rules.
    """

    def __init__(self, config: AcceleratorConfig):
        """

        :param config:
        """
        self.accelerator_config = config

    def read_current_schema(self, schema_type: str, schema_version: str = None) -> dict:
        """
        Read the current JSON schema
        :param schema_version str with the schema type as defined in the type matrix
        :return: json object representing schema
        """

        logger.info(f"Reading {schema_type} schema with version {schema_version}")
        type = self.accelerator_config.find_type_matrix_info_for_type(schema_type)
        json_schema = type.resolve_schema_version(schema_version)

        with determine_resource_path("accelerator_core.schema", json_schema) as fspath:
            logger.debug(f"resource path:{fspath}")
            with open(fspath) as json_data:
                d = json.load(json_data)
                return d

    def validate_json_against_schema(
        self, json_doc: dict, schema_type: str, schema_version: str = None
    ) -> SchemaValidationResult:
        """
        validate the given json (as a json dict)
        :param json_doc: dict with json to validate
        :param schema_version: version of accel schema to validate against, as a version string: 1.0.0,
        if left to None it will default to the default version
        :return: SchemaValidationResult
        """

        json_schema_doc = self.read_current_schema(schema_type, schema_version)
        try:
            jsonschema.validate(json_doc, json_schema_doc)
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"invalid json document {e}")
            schema_validation_result = SchemaValidationResult(
                False, schema_type, schema_version, json_doc, json_schema_doc, e
            )
            return schema_validation_result

        schema_validation_result = SchemaValidationResult(
            True, schema_type, schema_version, json_doc, json_schema_doc, None
        )
        return schema_validation_result
