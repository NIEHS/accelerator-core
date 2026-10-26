import json
import logging
import os
from collections.abc import Mapping
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template

logger = logging.getLogger(__name__)


class AccelTemplateProcessor:
    """
    Library for jinja templates for data models
    """

    def __init__(self):
        """
        Initialize ingest tool
        :return:
        """

        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Create a Jinja environment with the FileSystemLoader
        self.env = Environment(loader=FileSystemLoader(script_dir))
        self.env.filters["jsonify"] = json.dumps

    def retrieve_template(self, template_name: str, template_version: str) -> Template:
        """
        retrieve a template from the templates dir
        :param template_name: string with the template name as found in the templates dir, without version or extension
        :param template_version: string in x.x.x form with the version number
        :return: Template for jinja rendering
        """

        return self.env.get_template(f"{template_name}-v{template_version}.jinja")

    def render_generic(
        self,
        data: Any,
        submission: Mapping[str, Any] | Any,
        technical_metadata: Mapping[str, Any] | Any,
        template_version: str = "1.0.0",
    ) -> dict[str, Any]:
        """Render an arbitrary JSON document in the generic Accelerator shape."""

        template = self.retrieve_template("accel-generic", template_version)
        rendered = template.render(
            data=data,
            submission=self._to_dict(submission),
            technical_metadata=self._to_dict(technical_metadata),
        )
        return json.loads(rendered)

    @staticmethod
    def _to_dict(value: Mapping[str, Any] | Any) -> Any:
        if hasattr(value, "to_dict"):
            return value.to_dict()
        return value
