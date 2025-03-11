from abc import ABC, abstractmethod


class Crosswalk(ABC):
    """Abstract superclass for mapping raw data to a structured JSON format."""

    @abstractmethod
    def transform(self, raw_data: dict) -> dict:
        """Convert raw data into a standardized format."""
        pass
