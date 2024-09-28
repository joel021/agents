import re
import json

from agents.logger import logger


def extract_json(text: str) -> dict or None:

    try:
        return json.loads(text)
    except Exception as e:
        logger.error(str(e))
        return None

