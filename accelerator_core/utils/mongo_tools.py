"""
Tools for testing, including tools for test setup and teardown of databases and other utils in test
setup and teardown
"""

from pymongo import MongoClient

from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.resource_utils import determine_resource_path

logger = setup_logger("accelerator")

aip_collection = "aip_store"
temp_collection = "temp_store"


def build_connection_string(accel_config: AcceleratorConfig) -> str:
    """
    Build a mongo connection string from properties
         mongodb://user:xxxxx@localhost:27017/

    :param accel_config: AcceleratorConfig
    :return: str with the connection string

    """

    return f'mongodb://{accel_config.params["mongo.user"]}:{accel_config.params["mongo.password"]}@{accel_config.params["mongo.host"]}:{accel_config.params["mongo.port"]}/'


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
