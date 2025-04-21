"""
Dissemination support concrete implementation for Mongo data store
"""

from bson import ObjectId
from pipenv.patched.safety.formatter import NOT_IMPLEMENTED

from accelerator_core.schema.models.base_model import create_timestamped_log
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.services.dissemination import (
    Dissemination,
    DisseminationDescriptor,
    DisseminationPayload,
    DisseminationFilter,
)
from accelerator_core.utils.accel_database_utils import AccelDatabaseUtils
from accelerator_core.utils.accel_exceptions import AccelDocumentNotFoundException
from accelerator_core.utils.schema_tools import SchemaValidationResult
from accelerator_core.workflow.accel_source_ingest import (
    IngestSourceDescriptor,
    IngestPayload,
)
from accelerator_core.services.accession import Accession
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.logger import setup_logger

logger = setup_logger("accelerator")


class DisseminationMongo(Dissemination):
    """
    Concrete implementation of Dissemination
    """

    def __init__(
        self, accelerator_config: AcceleratorConfig, accel_db_context: AccelDbContext
    ):
        """
        Initialize the Accession sservice
        :param accelerator_config: AcceleratorConfig with general configuration
        :param accel_db_context: AccelDbContext that holds the db connection
        """
        Dissemination.__init__(self, accelerator_config)
        self.accel_db_context = accel_db_context
