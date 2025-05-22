class PayloadReporter:
    """
    Tool to differentially handle passing a result from an accelerator operation. This class either formats
    a response using xcom, or writes the result to a temporary directory and reports the path to the temorary
    data in the payload
    """

