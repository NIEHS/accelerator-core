import unittest
from unittest.mock import Mock

from bson import ObjectId

from accelerator_core.schema.models.base_model import WorkflowStatus
from accelerator_core.utils.accel_database_utils import AccelDatabaseUtils
from accelerator_core.utils.accel_exceptions import AccelDocumentNotFoundException


class TestWorkflowStatusUpdate(unittest.TestCase):
    def setUp(self):
        self.database_utils = AccelDatabaseUtils(None, None)
        self.collection = Mock()
        self.collection.name = "documents"
        self.document_id = str(ObjectId())

    def test_updates_status_and_appends_history(self):
        self.collection.update_one.return_value.matched_count = 1

        result = self.database_utils.update_workflow_status(
            self.collection, WorkflowStatus.REVIEWED, self.document_id
        )

        self.assertIs(result, self.collection.update_one.return_value)
        query, update = self.collection.update_one.call_args.args
        self.assertEqual(query, {"_id": ObjectId(self.document_id)})
        self.assertEqual(
            update["$set"]["technical_metadata.workflow_status"], "reviewed"
        )
        event = update["$push"]["technical_metadata.history"]
        self.assertIn("Workflow status changed to 'reviewed'", event["msg"])
        self.assertTrue(event["timestamp"])

    def test_accepts_status_value(self):
        self.collection.update_one.return_value.matched_count = 1

        self.database_utils.update_workflow_status(
            self.collection, "published", self.document_id
        )

        update = self.collection.update_one.call_args.args[1]
        self.assertEqual(
            update["$set"]["technical_metadata.workflow_status"], "published"
        )

    def test_rejects_invalid_status(self):
        with self.assertRaises(ValueError):
            self.database_utils.update_workflow_status(
                self.collection, "unrecognized", self.document_id
            )

        self.collection.update_one.assert_not_called()

    def test_raises_when_document_is_missing(self):
        self.collection.update_one.return_value.matched_count = 0

        with self.assertRaises(AccelDocumentNotFoundException):
            self.database_utils.update_workflow_status(
                self.collection, WorkflowStatus.ARCHIVED, self.document_id
            )


if __name__ == "__main__":
    unittest.main()
