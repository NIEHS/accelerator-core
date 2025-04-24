"""
Superclass transforms an accel record into a target format, this is the mirror image of the crosswalk operation on
ingest
"""

from accelerator_core.services.dissemination import (
    DisseminationDescriptor,
    DisseminationPayload,
)


class DisseminationTransform:
    """Abstract superclass for mapping accel data to a target format"""

    def transform(
        self, dissemination_request: DisseminationPayload
    ) -> DisseminationPayload:
        """
        convert the given accel data to a target format appropriate for dissemination, this is the mirror image
        of the crosswalk operation on ingest
        :param dissemination_request: DisseminationResult with details and content to be disseminated for a single
        document
        :return: DisseminationResult containing the transformed result and associated metadata. The result
        may be inline or may be via a path reference
        """
        pass
