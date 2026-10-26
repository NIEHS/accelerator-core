import unittest

from jinja2 import Template

from accelerator_core.schema.templates.template_processor import AccelTemplateProcessor


class TestTemplateProcessor(unittest.TestCase):

    def test_get_accel_template(self):
        templateProcessor = AccelTemplateProcessor()
        actual = templateProcessor.retrieve_template("accel", "1.0.3")
        self.assertIsInstance(actual, Template)

    def test_render_generic_document(self):
        template_processor = AccelTemplateProcessor()
        document = {"nested": {"value": "quoted \"text\""}, "items": [1, True]}

        actual = template_processor.render_generic(
            document,
            {
                "submitter_name": "Name",
                "submitter_email": "name@example.org",
                "submitter_comment": "",
            },
            {"original_source_type": "test", "history": []},
        )

        self.assertEqual(document, actual["data"])
        self.assertEqual("Name", actual["submission"]["submitter_name"])
        self.assertEqual("test", actual["technical_metadata"]["original_source_type"])
