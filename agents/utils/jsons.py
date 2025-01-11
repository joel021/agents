import json
import re

from agents.logger import logger


def extract_json(text: str) -> dict or None:
    try:
        json_match = re.search(r'{.*}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")
