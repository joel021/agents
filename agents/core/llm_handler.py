import google.generativeai as genai

from agents.utils.jsons import extract_json


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

    def generate_instructions(self, prompt: str, response_schema) -> str:
        return self.model.generate_content(prompt, generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=response_schema
        ),).text

    def generate_instructions_dict(self, prompt: str) -> dict:

        instructions_str = self.generate_instructions(self.generate_instructions(prompt))
        print(instructions_str)
        return extract_json(instructions_str)
