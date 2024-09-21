import google.generativeai as genai
import os

class GeminiHandler:

    def __init__(self, api_key: str, prompt_prefix: str, prompt_suffix: str) -> None:

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.prompt_prefix = prompt_prefix
        self.prompt_suffix = prompt_suffix

    def generate_instructions(self, prompt: str) -> str:
        
        response = self.model.generate_content(f"{self.prompt_prefix}{prompt}{self.prompt_suffix}")

        return response.text

