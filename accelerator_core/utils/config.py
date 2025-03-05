"""
Utilities related to configuration, resources and environment variables.
"""

import importlib.resources
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
