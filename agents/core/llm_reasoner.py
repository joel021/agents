import google.generativeai as genai

from agents.config import GEMINI_API_KEY, GPT_API_KEY
from agents.utils.jsons import extract_json


class LLMReasoner:

    def __init__(self):
        pass

    def simple_answer(self, prompt: str):
        raise NotImplementedError("Summary not implemented")

    def reason(self, prompt: str, response_schema: any) -> str:
        raise NotImplementedError("This is an abstract class")

    def reason_dict(self, prompt: str, response_schema: any) -> dict:
        raise NotImplementedError("This is an abstract class")


class GeminiReasoner(LLMReasoner):

    def __init__(self, api_key: str) -> None:
        super().__init__()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def reason(self, prompt: str, response_schema) -> str:
        return self.model.generate_content(prompt, generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=response_schema
        ),).text

    def reason_dict(self, prompt: str, response_schema) -> dict:

        instructions_str = self.reason(prompt, response_schema)
        return extract_json(instructions_str)

    def simple_answer(self, prompt: str) -> str:
        return self.model.generate_content(prompt).text


def get_new_llm_reasoner() -> LLMReasoner:
    if GEMINI_API_KEY:
        return GeminiReasoner(GEMINI_API_KEY)
    elif GPT_API_KEY:
        raise NotImplementedError("Gpt interfaces were not implemented yet.")

    raise NotImplementedError("No other options unless Gemini are available. Fill the GEMINI_API_KEY value.")
