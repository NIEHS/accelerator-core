"""
Misc utils for writing integration tests
"""

import json

from accelerator_core.utils.accel_database_utils import AccelDatabaseUtils

from accelerator_core.service_impls.accel_db_context import AccelDbContext

from accelerator_core.utils.accelerator_config import config_from_file

from accelerator_core.utils import resource_utils
from bson import json_util
from pymongo import MongoClient


def load_test_corpus():

    file_name = "test_corpus.json"

    test_path = resource_utils.determine_test_resource_path(
        "application.properties", "integration_tests"
    )

    matrix_path = resource_utils.determine_test_resource_path(
        "test_type_matrix.yaml", "tests"
    )

    config = config_from_file(test_path)
    accel_db_context = AccelDbContext(config)
    client = accel_db_context.mongo_client

    accel_database_utils = AccelDatabaseUtils(config, accel_db_context)

    type_matrix_info = config.find_type_matrix_info_for_type("accelerator")
    if not type_matrix_info:
        raise Exception(f"unknown document type")

    coll_name = type_matrix_info.collection
    collection = accel_db_context.db[coll_name]

    with open(file_name, "r", encoding="utf-8") as f:
        docs = json_util.loads(f.read())

        for doc in docs:
            doc.pop("_id", None)

        result = collection.insert_many(docs)
        print(f"Inserted {len(result.inserted_ids)} documents")
