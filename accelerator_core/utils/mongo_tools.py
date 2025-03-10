"""
Tools for testing, including tools for test setup and teardown of databases and other utils in test
setup and teardown
"""

from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.resource_utils import determine_resource_path

logger = setup_logger("accelerator")


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
