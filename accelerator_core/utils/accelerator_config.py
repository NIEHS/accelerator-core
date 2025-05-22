"""
Configuration Properties for accelerator core, typically configured as secrets or properties files
"""

from pathlib import Path

from coverage.annotate import os

import accelerator_core
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.resource_utils import properties_file_from_path
from accelerator_core.utils.type_matrix import TypeMatrix
from accelerator_core.utils.type_matrix import parse_type_matrix
from accelerator_core.utils.resource_utils import  determine_resource_path

logger = setup_logger("accelerator")


class AcceleratorConfig(object):
    """
    Configuration object for accelerator
    """

    def __init__(
        self,
        params:dict={}
    ):
        """
        Initialize the configuration with a dictionary of properties
            accelerator.xcom.tempfiles.supported:  True|False
            accelerator.xcom.tempfile.path: /opt/xcom or other
        """
        self.params = params

        self.type_matrix = parse_type_matrix(determine_resource_path("accelerator_core.schema",
                                                                     "type_matrix.yaml"))

        # see if ACCEL_MONGODB_PASSWORD is in env variables and replace the property with the env
        # variable.

        if os.environ.get("ACCEL_MONGODB_PASSWORD"):
            self.params["mongo.password"] = os.environ.get("ACCEL_MONGODB_PASSWORD")

    def find_type_matrix_info_for_type(self, type_name) -> TypeMatrix:
        """
        Find the type matrix info for a given type
        :param type_name: str with the type name in the type matrix
        :return: TypeMatrix that corresponds, or None if no type matrix is found
        """

        for type_matrix in self.type_matrix:
            if type_name == type_matrix.type:
                return type_matrix

        return None

def config_from_file(filepath) -> AcceleratorConfig:
    """
    Handy method to load accel config from a file
    """
    props = properties_file_from_path(filepath)
    accel_config = AcceleratorConfig(props)
    return accel_config

