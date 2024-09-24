import re
import json

def extract_json(text: str) -> dict:

    open_braces = text.find("{")
    close_braces = text.rfind("}")
    json_limited = text[open_braces:close_braces + 1]
    return json.loads(json_limited)
