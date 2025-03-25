from abc import ABC, abstractmethod

from accelerator_core.workflow.accel_source_ingest import (
    IngestSourceDescriptor,
    IngestResult,
)


class Crosswalk:
    """Abstract superclass for mapping raw data to a structured JSON format."""

    @abstractmethod
    def transform(self, ingest_result: IngestResult) -> dict:
        """Convert raw data into a standardized format.
        :param ingest_result: The ingest result.

        TODO: decide whether to make crosswalks a single doc task? How to handle more than one
        document during ingest - MC
        """
        pass
