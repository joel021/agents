import json

import google.generativeai as genai
import re

class LLMHandler:

    def __init__(self):
        pass

    def generate_instructions(self, prompt: str) -> str:
        raise NotImplementedError("This is an abstract class")

    def generate_instructions_dict(self, prompt: str) -> dict:
        raise NotImplementedError("This is an abstract class")


class GeminiHandler(LLMHandler):

    def __init__(self, api_key: str) -> None:
        super().__init__()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_instructions(self, prompt: str) -> str:
        return self.model.generate_content(prompt).text

    def generate_instructions_dict(self, prompt: str) -> dict:

        instructions_str = self.generate_instructions(self.generate_instructions(prompt))
        open_braces = instructions_str.find("{")
        close_braces = re.search(r"\}", instructions_str).start()

        return json.loads(instructions_str[open_braces:close_braces+1])

