"""
Tools and representation of the type matrix that relates a named type with the schema, collection,
temp collection and other type-specific hints.
"""

from pathlib import Path

from accelerator_core.utils.logger import setup_logger
import yaml

logger = setup_logger("accelerator")


class TypeMatrix:
    """
    Represents the configuration of a type
    """

    def __init__(
        self,
        type: str,
        schema: str,
        default_schema_version: str,
        collection: str,
        temp_collection: str,
    ):
        self.type = type
        self.schema = schema
        self.default_schema_version = default_schema_version
        self.collection = collection
        self.temp_collection = temp_collection

    def resolve_schema_version(self, version: str = None) -> str:
        """
        give the fully parsed schema name
        :param version: optional version, otherwise defaulting to the default_schema_version
        :return: str with the fully parsed schema name
        """

        if version is None:
            resolved_version = self.default_schema_version
        else:
            resolved_version = version

        return f"{self.schema}-v{resolved_version}.json"


def parse_type_matrix(type_matrix_path: Path) -> [TypeMatrix]:
    """
    Given a path to a type_matrix def, parse it
    :param type_matrix_path: str with full path to type matrix
    :return: TypeMatrix[]
    """
    logger.info(f"Parsing type matrix from {type_matrix_path}")
    matrix = []
    with open(type_matrix_path, "r") as stream:
        val = yaml.safe_load(stream)

        for type in val["types"]:
            matrix.append(
                TypeMatrix(
                    type["name"],
                    type["schema"],
                    type["default_version"],
                    type["collection"],
                    type["temp_collection"],
                )
            )

        return matrix
