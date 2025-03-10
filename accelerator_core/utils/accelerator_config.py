"""
Configuration Properties for accelerator core, typically configured as secrets or properties files
"""

from coverage.annotate import os

from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.resource_utils import properties_file_from_path

logger = setup_logger("accelerator")


class AcceleratorConfig(object):
    """
    Configuration object for accelerator

    """

    def __init__(self, config_path=None, config_env="ACCELERATOR_CONFIG"):
        """
        Create an accelerator configuration object, either by specifying a path or an environment variable
        that points to the path of the configuration properties
        :param config_path: optional, defaults to None, is the absolute path to the config.properties
        :param config_env: optional, defaults to 'ACCELERATOR_CONFIG', is an env variable that contains the
        absolute path to the config.properties file
        """

        if config_path is not None:
            logger.info(f"loading accelerator config from {config_path}")
            self.properties = properties_file_from_path(config_path)
        else:
            logger.info(
                f"loading accelerator config from environment variable {config_env}"
            )
            env_path = os.environ.get(config_env)
            self.properties = properties_file_from_path(env_path)
