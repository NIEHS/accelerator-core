"""
Custom Accel exception types
"""


class AccelDocumentNotFoundException(Exception):
    """
    A document was not found in accel
    """

    def __init__(self, document_id: str, document_type: str, temp_doc: bool):
        super().__init__(
            f"Document id: {document_id} not found in type {document_type}, temp doc? {temp_doc}"
        )
        self.document_id = document_id
        self.document_type = document_type
        self.temp_doc = temp_doc
