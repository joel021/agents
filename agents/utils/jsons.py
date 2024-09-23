import re
import json

def extract_json(text: str) -> dict:

    open_braces = text.find("{")
    close_braces = text.rfind("}")

    return json.loads(text[open_braces:close_braces + 1])
