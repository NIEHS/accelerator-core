"""
Accession support concrete implementation for Mongo data store
"""

from accelerator_core.services.accession import Accession
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.schema_tools import CURRENT_ACCEL_SCHEMA_VERSION
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.schema_tools import validate_json_against_schema

logger = setup_logger("accelerator")


class AccessionMongo(Accession):
    """
    Accession module based on Mongo persistence
    """

    def __init__(self, acclerator_config: AcceleratorConfig):
        Accession.__init__(self, acclerator_config)

    def validate(
        self, json_dict: dict, schema_version: str = CURRENT_ACCEL_SCHEMA_VERSION
    ) -> bool:
        return super().validate(json_dict, schema_version)

    def create(self) -> str:
        return super().create()

    def read(self, record_id: str) -> dict:
        return super().read(record_id)

    def update(self, record_id: str, new_data: dict) -> bool:
        return super().update(record_id, new_data)

    def delete(self, record_id: str) -> bool:
        return super().delete(record_id)
