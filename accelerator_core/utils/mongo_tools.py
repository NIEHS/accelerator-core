"""
Tools for testing, including tools for tests setup and teardown of databases and other utils in tests
setup and teardown
"""

import json
import logging

from bson import json_util
from bson.json_util import CANONICAL_JSON_OPTIONS
from pymongo import MongoClient, ASCENDING

from accelerator_core.utils.accelerator_config import AcceleratorConfig

logger = logging.getLogger(__name__)

aip_collection = "aip_store"
temp_collection = "temp_store"


def is_mongo_direct(accel_config: AcceleratorConfig) -> bool:
    """
    Determines if the given accelerator configuration uses a direct MongoDB connection.

    This function evaluates whether the provided `AcceleratorConfig` object is
    configured for direct communication with MongoDB, returning a boolean result.

    Args:
        accel_config (AcceleratorConfig): The configuration object for the accelerator.

    Returns:
        bool: True if the accelerator configuration uses a direct MongoDB connection,
        False otherwise.
    """

    mongo_direct = accel_config.params.get("mongo.direct", None)

    if not mongo_direct:
        return False

    val = mongo_direct.lower() == "true"
    return val


def build_connection_string(accel_config: AcceleratorConfig) -> str:
    """
    Build a mongo connection string from properties
         mongodb://user:xxxxx@localhost:27017/

    :param accel_config: AcceleratorConfig
    :return: str with the connection string

    """

    mongo_direct = is_mongo_direct(accel_config)
    conn = f'mongodb://{accel_config.params["mongo.user"]}:{accel_config.params["mongo.password"]}@{accel_config.params["mongo.host"]}:{accel_config.params["mongo.port"]}/'

    if accel_config.params.get("mongo.replicaset", None):
        logger.info(f"repl: {accel_config.params['mongo.replicaset']}")

        conn += (
            f"?replicaSet={accel_config.params['mongo.replicaset']}&authSource=admin"
        )

        if mongo_direct:
            conn += "&directConnection=true"

    else:
        if mongo_direct:
            conn += "?directConnection=true"

    logger.info(f"connection string: {conn}")

    return conn


def initialize_mongo_client(accel_config: AcceleratorConfig) -> MongoClient:
    """
    Obtain a mongo client connection given the current configuration
    :param accel_config: AcceleratorConfig
    :return: MongoClient with connection
    """

    connection_string = build_connection_string(accel_config)
    return MongoClient(connection_string)


def drop_accel_database(mongo_client: MongoClient, db_name: str) -> None:
    """Drop the accelerator database
    :param mongo_client: MongoClient
    :param db_name: str
    """
    logger.info(f"dropping database: {db_name}")
    db = mongo_client.get_database(db_name)
    db.command({"dropDatabase": 1})
    logger.info("dropped!")


def create_accel_database(mongo_client: MongoClient, db_name: str) -> None:
    """Create the accelerator database
    :param mongo_client: MongoClient
    :param db_name: str
    """

    logger.info(f"creating database: {db_name}")
    db = mongo_client[db_name]
    db.create_collection(aip_collection)
    db.create_collection(temp_collection)

    logger.info("created!")


def create_accel_indexes(
    accel_config: AcceleratorConfig,
    mongo_client: MongoClient,
    db_name: str,
    matrix_type: str,
) -> None:

    logger.info(f"creating indexes: {aip_collection}")

    type_info = accel_config.find_type_matrix_info_for_type(matrix_type)

    db = mongo_client[db_name]
    coll = db[type_info.collection]
    index_name = coll.create_index(
        [
            ("technical_metadata.original_source_link", ASCENDING),
            ("technical_metadata.original_source_identifier", ASCENDING),
        ],
        unique=True,
    )
    logger.info(f"created index {index_name}")

    if type_info.temp_collection:
        logger.info(f"index for temporary collection {type_info.temp_collection}")
        coll = db[type_info.temp_collection]
        index_name = coll.create_index(
            [
                ("technical_metadata.original_source_link", ASCENDING),
                ("technical_metadata.original_source_identifier", ASCENDING),
            ],
            unique=True,
        )
        logger.info(f"created index {index_name}")


def convert_doc_to_json(doc: dict) -> dict:
    """
    Take a dict that is a document from Mongo query and turn it into standard json
    """
    docstr = json_util.dumps(doc, json_options=CANONICAL_JSON_OPTIONS)
    return json.loads(docstr)
