from accelerator_core.utils.accelerator_config import AcceleratorConfig
from accelerator_core.utils.mongo_tools import initialize_mongo_client

"""
Context object passed to services, wraps the db connections
"""


class AccelDbContext(object):
    """
    Database context for services, wraps the db connections
    """

    def __init__(self, accelerator_config: AcceleratorConfig):
        self.accelerator_config = accelerator_config
        self.mongo_client = initialize_mongo_client(self.accelerator_config)
        self.db = self.mongo_client.get_database(
            self.accelerator_config.params["mongo.db.name"]
        )
