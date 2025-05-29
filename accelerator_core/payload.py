class Payload:
    """
    Represents a payload passed between tasks
    """

    def __init__(self, payload=[], payload_path=[], payload_inline=True):
        """
        common payload elements
        :param payload: an array of inline data
        :param payload_path: an array of paths to serialized data (temp files)
        :param payload_inline: bool indicating whether payload is inline
        """

        self.payload = payload
        self.payload_path = payload_path
        self.payload_inline = payload_inline
