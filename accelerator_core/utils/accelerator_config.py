"""
Configuration Properties for accelerator core, typically configured as secrets or properties files
"""

from pathlib import Path

from coverage.annotate import os

from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.resource_utils import properties_file_from_path
from accelerator_core.utils.type_matrix import TypeMatrix
from accelerator_core.utils.type_matrix import parse_type_matrix

logger = setup_logger("accelerator")


class AcceleratorConfig(object):
    """
    Configuration object for accelerator
    """

    def __init__(
        self,
        config_path: str = None,
        config_env: str = "ACCELERATOR_CONFIG",
        type_matrix_path: str = None,
        type_matrix_env: str = "ACCELERATOR_TYPE_MATRIX_PATH",
    ):
        """
        Create an accelerator configuration object, either by specifying a path or an environment variable
        that points to the path of the configuration properties
        :param config_path: optional, defaults to None, is the absolute path to the config.properties
        :param config_env: optional, defaults to 'ACCELERATOR_CONFIG', is an env variable that contains the
        absolute path to the config.properties file
        :param type_matrix_path: optional, defaults to None, is the absolute path to the type_matrix
        :param type_matrix_env: optional, defaults to None, is an env variable that contains the
        path to the type matrix, overridden if a path is given
        """

        # try to get config by env, then given path, then fail
        env_path = os.environ.get(config_env, None)

        if not env_path:
            env_path = config_path

        if not env_path:
            raise Exception(
                "missing ACCELERATOR_CONFIG env variable or a config_path variable"
            )

        self.properties = properties_file_from_path(env_path)

        # try to get matrix path by env, then given path, then fail

        matrix_path = os.environ.get(type_matrix_env, None)

        if not matrix_path:
            matrix_path = type_matrix_path

        if not matrix_path:
            raise Exception(
                "missing ACCELERATOR_TYPE_MATRIX_PATH env variable or a type_matrix_path variable"
            )

        self.type_matrix = parse_type_matrix(Path(matrix_path))

        # see if ACCEL_MONGODB_PASSWORD is in env variables and replace the property with the env
        # variable.

        if os.environ.get("ACCEL_MONGODB_PASSWORD"):
            self.properties["mongo.password"] = os.environ.get("ACCEL_MONGODB_PASSWORD")

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
