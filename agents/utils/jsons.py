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


def decode_message(message) -> dict | None:
    if message['type'] == 'message':
        if isinstance(message['data'], bytes):
            decoded_message = message['data'].decode('utf-8')
        else:
            decoded_message = message['data']
        return json.loads(decoded_message)

    return None
