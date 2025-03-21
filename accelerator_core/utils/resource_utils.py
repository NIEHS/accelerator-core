"""
Utilities related to configuration, resources and environment variables.
"""

import importlib.resources
import os
from pathlib import Path
from accelerator_core.utils.logger import setup_logger
import json

logger = setup_logger("accelerator")


def determine_resource_path(resource_package, resource_name) -> Path:
    """
    Given a package and resource name, get the given program resource
    :param resource_package: package where resources are located
    :param resource_name: name of the resource in the package
    :return: Path object to the resource
    """

    with importlib.resources.path(resource_package, resource_name) as fspath:
        logger.debug(f"resource path:{fspath}")
        return fspath


def determine_test_resource_path(resource_name: str, test_class: str = "tests") -> Path:
    """
    Given a file name, find that file in the test_resources
    :param resource_name: name of the resource file
    :param test_class: location in either 'tests' or 'integration_tests'
    :return: Path object to the resource
    """

    dir = Path(os.path.dirname(__file__)).parent.parent
    filename = os.path.join(dir, f"{test_class}/test_resources/{resource_name}")
    return Path(filename)


def properties_file_from_path(filename):
    """
    Create a dictionary from a properties file at the given absolute path
    :param filename: absolute path to the properties file
    :return: dict of the properties
    """
    logger.debug("properties_file_from_path()")
    logger.debug("filename: %s" % filename)

    my_props = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()  # removes trailing whitespace and '\n' chars

            if "=" not in line:
                continue  # skip blanks and comments w/o =
            if line.startswith("#"):
                continue  # skip comments which contain =

            k, v = line.split("=", 1)
            my_props[k] = v

    return my_props


def properties_file_from_env(env_location):
    """
    Given an env variable that points to a file absolute path, retrieve the properties file and
    make it a dict
    :param env_location: env variable name with an absolute path to a properties file
    :return: dict with the properties
    """
    file_name = os.environ[env_location]
    if file_name is None:
        raise Exception(
            f"No properties file located via environment variable {env_location}"
        )
    return properties_file_from_path(file_name)
