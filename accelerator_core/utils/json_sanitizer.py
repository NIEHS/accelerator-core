from typing import Union, Dict, Any
import html
import json
import re

class JSONSanitizer:
    @staticmethod
    def sanitize_json_string(json_str: str) -> Union[Dict, list]:
        # Step 1: Replace Python-style values with valid JSON
        fixed_str = JSONSanitizer._preprocess_python_style_json(json_str)

        # Step 2: Parse as JSON
        try:
            parsed_data = json.loads(fixed_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string after preprocessing: {e}")

        # Step 3: Sanitize all values
        return JSONSanitizer._sanitize(parsed_data)

    @staticmethod
    def _preprocess_python_style_json(json_str: str) -> str:
        # Replace None → ""
        json_str = re.sub(r'(:\s*)None\b', r'\1""', json_str)

        # Replace True → true
        json_str = re.sub(r'(:\s*)True\b', r'\1true', json_str)

        # Replace False → false
        json_str = re.sub(r'(:\s*)False\b', r'\1false', json_str)

        return json_str

    @staticmethod
    def _sanitize(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {
                k: JSONSanitizer._sanitize(v if v is not None else "")
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [JSONSanitizer._sanitize(item) for item in obj]
        elif isinstance(obj, str):
            return JSONSanitizer._clean_string(obj)
        else:
            return obj

    @staticmethod
    def _clean_string(s: str) -> str:
        s = s.strip()
        s = html.unescape(s)
        s = re.sub(r'<[^>]+>', '', s)
        s = re.sub(r'[\r\n]+', ' ', s)
        s = re.sub(r'[^\w\s\-.,:/]', '', s)
        s = re.sub(r'\s+', ' ', s)
        return s.strip()