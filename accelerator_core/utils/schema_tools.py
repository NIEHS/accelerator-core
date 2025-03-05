import importlib.resources

from accelerator_core.utils.logger import setup_logger
import accelerator_core.schema
from accelerator_core.utils.config import determine_resource_path
import json
import jsonschema

logger = setup_logger("accelerator")

CURRENT_ACCEL_SCHEMA_VERSION = "1.0.0"
CURRENT_JSON_SCHEMA_VERSION = "2020-12"


def read_current_schema(schema_version: str = CURRENT_ACCEL_SCHEMA_VERSION):
    """
    Read the current JSON schema
    :param schema_version: n.n.n schema version (defaults to most current)
    :return: json object representing schema
    """

    schema_name = f"accel-schema-v{schema_version}.json"

    with determine_resource_path(accelerator_core.schema, schema_name) as fspath:
        logger.debug(f"resource path:{fspath}")
        with open(fspath) as json_data:
            d = json.load(json_data)
            return d


def validate_json_against_schema(
    json_doc, schema_version: str = CURRENT_ACCEL_SCHEMA_VERSION
) -> bool:
    """
    validate the given json (as a json dict)
    :param json_doc: dict with json to validate
    :param schema_version: version of accel schema to validate against, as a version string: 1.0.0
    :return: bool is True if valid
    """

    json_schema_doc = read_current_schema(schema_version)
    try:
        jsonschema.validate(json_doc, json_schema_doc)
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"invalid json document {e}")
        return False

    return True
