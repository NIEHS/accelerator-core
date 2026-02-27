import logging

from bson import ObjectId

from accelerator_core.schema.models.base_model import DisseminationLinkReport
from accelerator_core.service_impls.accel_db_context import AccelDbContext
from accelerator_core.services.dissemination_reporter import DisseminationReporter
from accelerator_core.utils.accel_database_utils import AccelDatabaseUtils
from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.xcom_utils import XcomPropsResolver

logger = logging.getLogger(__name__)


class MongoDisseminationReporter(DisseminationReporter):
    """
    Concrete implementation of DisseminationReporter for mongo, this will record linkages to deployed
    endpoints from a record in the accel db. This is a task to be added at the tail end of a dissemination DAG
    """

    def __init__(
        self,
        accelerator_config: AcceleratorConfig,
        xcom_properties_resolver: XcomPropsResolver,
        accel_db_context: AccelDbContext,
    ):
        """
        Initialize the Accession sservice
        @param accelerator_config: AcceleratorConfig with general configuration
        @param accel_db_context: AccelDbContext that holds the db connection
        """
        super().__init__(accelerator_config, xcom_properties_resolver)
        self.accel_db_context = accel_db_context
        self.accel_database_utils = AccelDatabaseUtils(
            accelerator_config, accel_db_context
        )

    def report_dissemination_result(
        self, dissemination_link_report: DisseminationLinkReport
    ):
        """
        After accessioning a record to a dissemination endpoint, this task can receive the report
        of the endpoint operation and link the dissemination endpoint to the accelerator model record.

        The input DisseminationLinkReport is the output of the dissemination service and can contain
        a success flag and error message. This task should consult before attempting the link.

        The DisseminationLinkReport should contain information to identify the accel record along with (hopefully)
        information that could identify the location of the dissemination. In an ideal case
        one should be able to go from accelerator to the actual location, but there may be cases
        where only partial information is possible, so we do the best we can.

        @param dissemination_link_report:DisseminationLinkReport with the output of the dissemination
        attempt
        """

        logger.info(f"report_dissemination_result({dissemination_link_report})")
        if not dissemination_link_report.success:
            logger.warning("unsuccessful dissemination, not reporting")
            logger.warning(f"message: {dissemination_link_report.message}")
            return

        with self.accel_db_context.start_session() as session:
            with session.start_transaction():
                try:
                    doc = self.accel_database_utils.find_by_id(
                        dissemination_link_report.original_source_identifier,
                        dissemination_link_report.target_schema_type,
                        dissemination_link_report.temporary_data,
                        session=session,
                    )

                    endpoints = doc["technical_metadata"]["dissemination_endpoints"]
                    matched = False

                    for endpoint in endpoints:
                        if (
                            endpoint["endpoint_type"]
                            == dissemination_link_report.dissemination_endpoint.endpoint_type
                        ):
                            logger.info("found id, updating dissemination date")
                            collection = (
                                self.accel_database_utils.build_collection_reference(
                                    dissemination_link_report.target_schema_type,
                                    dissemination_link_report.temporary_data,
                                )
                            )
                            # For updating an existing endpoint
                            update_operation = {
                                "$set": {
                                    "technical_metadata.dissemination_endpoints.$[elem].date": dissemination_link_report.dissemination_endpoint.date
                                }
                            }

                            result = collection.update_one(
                                {
                                    "_id": ObjectId(
                                        dissemination_link_report.original_source_identifier
                                    )
                                },
                                update_operation,
                                array_filters=[
                                    {
                                        "elem.endpoint_type": dissemination_link_report.dissemination_endpoint.endpoint_type
                                    }
                                ],
                                session=session,
                            )

                            matched = True

                    if not matched:
                        logger.info("adding new endpoint")

                        # For adding a new endpoint
                        update_operation = {
                            "$push": {
                                "technical_metadata.dissemination_endpoints": dissemination_link_report.dissemination_endpoint.to_dict()
                            }
                        }
                        collection = (
                            self.accel_database_utils.build_collection_reference(
                                dissemination_link_report.target_schema_type,
                                dissemination_link_report.temporary_data,
                            )
                        )
                        result = collection.update_one(
                            {
                                "_id": ObjectId(
                                    dissemination_link_report.original_source_identifier
                                )
                            },
                            update_operation,
                        )

                except Exception as e:
                    # Transaction is automatically aborted if an exception occurred within the 'with' block
                    print(f"Transaction aborted due to an error: {e}")
