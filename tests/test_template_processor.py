import json
import unittest

from jinja2 import Template

from accelerator_core.schema.templates.template_processor import AccelTemplateProcessor


class TestTemplateProcessor(unittest.TestCase):

    def test_get_accel_template(self):
        templateProcessor = AccelTemplateProcessor()
        actual = templateProcessor.retrieve_template("accel", "1.0.0")
        self.assertIsInstance(actual, Template)
